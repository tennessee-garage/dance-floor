import os
import time
import threading
from flask import Flask, jsonify, request, abort, render_template, send_from_directory

from floor.controller import Controller
from floor.controller.playlist import ProcessorNotFound

MIN_BPM = 40
MAX_BPM = 220

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, root_path=BASE_DIR)
app.controller = None  # type: Controller


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/layout')
def layout():
    return render_template('layout.html', nav="layout")


@app.route('/static/<path:path>')
def static_assets(path):
    return send_from_directory('static', path)


def view_playlist(playlist):
    if playlist.next_advance is not None:
        remain = max(0, playlist.next_advance - time.time())
    else:
        remain = 0
    remain_millis = int(remain * 1000)
    return {
        'current_position': playlist.position,
        'millis_remaining': remain_millis,
        'queue': playlist.queue,
    }


def view_tempo(bpm, downbeat):
    return {
        'bpm': bpm,
        'downbeat_millis': int(downbeat * 1000)
    }


def view_processors(processors):
    ret = {}
    for k, v in processors.iteritems():
        ret[k] = {
            'name': k,
        }
    return ret


def view_all_layers(layers):
    result = {}
    for k, v in layers.items():
        if k == 'playlist':
            continue
        result[k] = view_processor_layer(v)
    return result


@app.route('/api/status', methods=['GET'])
def api_status():
    result = {
        'playlist': view_playlist(app.controller.playlist),
        'tempo': view_tempo(app.controller.bpm, app.controller.downbeat),
        'processors': view_processors(app.controller.all_processors),
        'layers': view_all_layers(app.controller.layers),
    }
    return jsonify(result)


@app.route('/api/playlist', methods=['GET'])
def api_playlist():
    playlist = app.controller.playlist
    return jsonify(view_playlist(playlist))


@app.route('/api/playlist/start', methods=['POST'])
def api_playlist_start():
    playlist = app.controller.playlist
    playlist.start_playlist()
    return jsonify(view_playlist(playlist))


@app.route('/api/playlist/stop', methods=['POST'])
def api_playlist_stop():
    playlist = app.controller.playlist
    playlist.stop_playlist()
    return jsonify(view_playlist(playlist))


@app.route('/api/playlist/advance', methods=['POST'])
def api_playlist_advance():
    playlist = app.controller.playlist
    playlist.advance()
    return jsonify(view_playlist(playlist))


@app.route('/api/playlist/previous', methods=['POST'])
def api_playlist_previous():
    playlist = app.controller.playlist
    playlist.previous()
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

    playlist = app.controller.playlist
    try:
        if play_next:
            position = playlist.append(name, duration, args)
        else:
            position = playlist.insert_next(name, duration, args)
    except ProcessorNotFound as e:
        abort(400, str(e))
        return

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


@app.route('/api/tempo', methods=['GET', 'POST'])
def api_tempo():
    controller = app.controller
    if request.method == 'POST':
        content = request.get_json(silent=True)
        bpm = float(content.get('bpm', 0))
        if not bpm:
            abort(400, 'Must give bpm.')
        controller.set_bpm(bpm)

    return jsonify(view_tempo(controller.bpm, controller.downbeat))


@app.route('/api/tempo/nudge', methods=['POST'])
def api_tempo_nudge():
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


@app.route('/api/brightness', methods=['GET', 'POST'])
def api_brightness():
    controller = app.controller
    if request.method == 'POST':
        content = request.get_json(silent=True)
        brightness = content.get('brightness')
        if brightness is None:
            abort(400, 'Must give brightness.')
        brightness = float(brightness)
        if brightness < 0.0 or brightness > 1.0:
            abort(400, 'Value must be on range 0.0-1.0')
        controller.set_brightness(brightness)

    return jsonify({'brightness': controller.brightness})


@app.route('/api/layout', methods=['POST'])
def api_layout():
    """
    Updates the floor layout for when tiles have been bridged or are missing
    :return:
    """
    pass


def view_processor_layer(layer):
    return {
        'enabled': layer.is_enabled(),
        'processor_name': layer.get_processor_name(),
    }


@app.route('/api/layers/<string:layer_name>', methods=['GET', 'PATCH'])
def api_layer_detail(layer_name):
    if layer_name == 'playlist':
        abort(400, 'Playlist layer is not supported by this API.')
        return

    layer = app.controller.layers.get(layer_name)
    if not layer:
        abort(404, 'Unknown layer.')
        return

    if request.method == 'PATCH':
        content = request.get_json(silent=True)

        enabled = content.get('enabled')
        if enabled is not None:
            layer.set_enabled(enabled)

        processor_name = content.get('processor_name')
        if processor_name == '':
            layer.set_processor(None)
        else:
            processor = app.controller.all_processors.get(processor_name)
            if not processor:
                abort(400, 'Processor "{}" not found'.format(processor_name))
                return
            layer.set_processor(processor())

    return jsonify(view_processor_layer(layer))


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
