from builtins import map
from gevent import monkey
monkey.patch_all()

import os
import collections
import threading
import json
import logging
import time
logger = logging.getLogger('devserver')

import gevent
from geventwebsocket.handler import WebSocketHandler

from flask import Flask
from flask import render_template, request
from flask_sockets import Sockets

from floor.driver.base import Base
from floor.processor.constants import COLOR_MAXIMUM

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'devserver')

app = Flask(__name__, root_path=BASE_DIR, template_folder=TEMPLATE_DIR)
sockets_app = Sockets(app)

WAITER = gevent.event.Event()
MESSAGE_QUEUE = collections.deque()
SOCKETS = set()

FAKE_WEIGHTS = [0] * 64
WEIGHT_ON_SECONDS = 1.0


@sockets_app.route('/events')
def echo_socket(ws):
    logger.info('Socket connected: {}'.format(ws))
    SOCKETS.add(ws)
    try:
        while not ws.closed:
            message = ws.receive()
            if not message:
                continue
            try:
                message = json.loads(message)
            except ValueError:
                logger.warning('Ignoring unparseable JSON message: "{}"'.format(message))
            logger.info('Got message: {}'.format(message))
            if message.get('event') == 'click':
                pixel = message.get('payload', {}).get('pixel', None)
                if pixel is not None and pixel <= 64 and pixel >= 0:
                    FAKE_WEIGHTS[pixel] = time.time()
    finally:
        SOCKETS.remove(ws)
    logger.info('Socket disconnected.')


@app.route('/')
def devserver_main():
    # "Embedded" mode means the devserver is being shown in an iframe, eg
    # from the control server. The template will hide some things in this mode.
    is_embedded = request.args.get('is_embedded', '') == 'true'
    return render_template('index.html', is_embedded=is_embedded)


def sender():
    while True:
        WAITER.wait()
        WAITER.clear()
        while MESSAGE_QUEUE:
            message = json.dumps(MESSAGE_QUEUE.popleft())
            for socket in SOCKETS:
                socket.send(message)


def _broadcast(message):
    MESSAGE_QUEUE.append(message)
    WAITER.set()


def serve_forever(port=1979):
    logger.info('Starting devserver on port {}'.format(port))
    gevent.spawn(sender)
    server = gevent.pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    server.serve_forever()


class Devserver(Base):
    """Floor driver interface."""

    def __init__(self, args):
        super(Devserver, self).__init__(args)
        self.weights = [0] * 64
        self.thr = threading.Thread(target=serve_forever)
        self.thr.daemon = True
        self.thr.start()

    @classmethod
    def rescale_color_value(cls, color_value):
        """Convert processor pixels to CSS-compatible values on [0, 256)."""
        return (color_value / float(COLOR_MAXIMUM)) * 256.0

    def send_data(self):
        leds = [list(map(self.rescale_color_value, pixel)) for pixel in self.leds]
        message = {
            "event": "leds",
            "payload": leds,
        }
        _broadcast(message)

    def read_data(self):
        pass

    def get_weights(self):
        now = time.time()
        values = [1 if (now - t) <= WEIGHT_ON_SECONDS else 0 for t in FAKE_WEIGHTS]
        return values
