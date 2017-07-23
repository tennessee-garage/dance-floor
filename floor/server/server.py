import time
import threading
from flask import Flask, jsonify, request, abort, render_template, send_from_directory

MIN_BPM = 40
MAX_BPM = 220

app = Flask('server')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_assets(path):
    return send_from_directory('static', path)

def view_playlist(playlist):
    if playlist.next_advance is not None:
        remain = max(0, playlist.next_advance - time.time())
    else:
        remain = 0
    return {
        'current_position': playlist.position,
        'millis_remaining': remain,
        'queue': playlist.queue,
    }

def view_tempo(bpm, downbeat):
    return {
        'bpm': bpm,
        'downbeat_millis': int(downbeat * 1000)
    }

@app.route('/api/playlist', methods=['GET'])
def api_playlist():
    playlist = app.controller.playlist
    return jsonify(view_playlist(playlist))

@app.route('/api/playlist/advance', methods=['POST'])
def api_playlist_advance():
    playlist = app.controller.playlist
    playlist.advance()
    return jsonify(view_playlist(playlist))

@app.route('/api/playlist/add', methods=['POST'])
def api_playlist_add():
    content = request.get_json(silent=True)
    name = content.get('name')
    args = content.get('args')
    duration = int(content.get('duration', 0))
    immediate = content.get('immediate', False)
    play_next = content.get('next', False) or immediate

    if not name:
        abort(400, 'Missing `name` parameter.')

    # Validate args... sorta :-x
    try:
        app.controller.build_processor(name, args)
    except ValueError as e:
        abort(400, str(e))

    playlist = app.controller.playlist
    if play_next:
        position = playlist.append(name, duration, args)
    else:
        position = playlist.insert_next(name, duration, args)

    if immediate:
        playlist.go_to(position)

    return jsonify(view_playlist(playlist))

@app.route('/api/playlist/stay', methods=['POST'])
def api_playlist_stay():
    playlist = app.controller.playlist
    app.controller.playlist.stay()
    return jsonify(view_playlist(playlist))

@app.route('/api/playlist/<int:position>', methods=['GET', 'DELETE'])
def api_playlist_position(position):
    playlist = app.controller.playlist
    if request.method == 'DELETE':
        try:
            playlist.remove(position)
        except ValueError as e:
            abort(400, str(e))
        return jsonify(view_playlist(playlist))
    else:
        return jsonify(playlist.queue[position])

@app.route('/api/bpm', methods=['GET', 'POST'])
def api_bpm():
    controller = app.controller
    if request.method == 'POST':
        content = request.get_json(silent=True)
        bpm = float(content.get('bpm', 0))
        if not bpm:
            abort(400, 'Must give bpm.')
        controller.set_bpm(bpm)

    return jsonify(view_tempo(controller.bpm, controller.downbeat))

@app.route('/api/bpm/nudge', methods=['POST'])
def api_bpm_nudge_downbeat():
    controller = app.controller
    content = request.get_json(silent=True)

    bpm_delta = 0
    if content.get('bpm_delta') is not None:
        bpm_delta = float(content.get('bpm_delta', 0))

    downbeat_millis_delta = 0
    if content.get('downbeat_millis_delta') is not None:
        downbeat_millis_delta = float(content.get('downbeat_millis_delta', 0))

    bpm = controller.bpm + bpm_delta
    downbeat = controller.downbeat + (downbeat_millis_delta / 1000.0)

    if bpm < MIN_BPM or bpm > MAX_BPM:
        abort(400, 'Crazy bpm.')

    controller.set_bpm(bpm, downbeat)
    return jsonify(view_tempo(controller.bpm, controller.downbeat))

def run_server(controller, host='0.0.0.0', port=1977, debug=True):
    app.controller = controller
    thr = threading.Thread(target=app.run, kwargs={
        'host': host,
        'port': port,
        'debug': debug,
        'use_reloader': False,
    })
    thr.daemon = True
    app.logger.info('Starting server on http://{}:{}'.format(host, port))
    thr.start()
