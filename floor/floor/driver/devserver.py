from gevent import monkey
monkey.patch_all()

import os
import collections
import threading
import json
import logging
logger = logging.getLogger('devserver')

import gevent
from geventwebsocket.handler import WebSocketHandler

from flask import Flask
from flask import render_template
from flask_sockets import Sockets

from floor.driver.base import Base

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'devserver')

app = Flask(__name__, root_path=BASE_DIR, template_folder=TEMPLATE_DIR)
sockets_app = Sockets(app)

WAITER = gevent.event.Event()
MESSAGE_QUEUE = collections.deque()
SOCKETS = set()

@sockets_app.route('/events')
def echo_socket(ws):
    logger.info('Socket connected: {}'.format(ws))
    SOCKETS.add(ws)
    try:
        while not ws.closed:
            message = ws.receive()
            logger.info('Got message: {}'.format(message))
    finally:
        SOCKETS.remove(ws)
    logger.info('Socket disconnected.')

@app.route('/')
def hello():
    return render_template('index.html')

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
        self.weights = [0] * 64
        self.thr = threading.Thread(target=serve_forever)
        self.thr.daemon = True
        self.thr.start()

    def send_data(self):
        # Ensure all RGB values are integral.
        leds = [map(int, pixel) for pixel in self.leds]
        message = {
            "event": "leds",
            "payload": leds,
        }
        _broadcast(message)

    def read_data(self):
        pass

    def get_weights(self):
        return self.weights
