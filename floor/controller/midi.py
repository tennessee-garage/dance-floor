from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import threading
from pymidi import server as pymidi_server


class MidiFunctions:
    """Simple listing of functions that are controllable through Midi."""

    PLAYLIST_NEXT = 'playlist_next'
    PLAYLIST_PREVIOUS = 'playlist_previous'
    PLAYLIST_PAUSE = 'playlist_pause'
    PLAYLIST_PLAY = 'playlist_play'
    PLAYLIST_STAY = 'playlist_stay'
    PLAYLIST_STOP = 'playlist_stop'
    SET_BPM = 'set_bpm'


NOTE_ON = 'NOTE_ON'
CONTROL_MODE_CHANGE = 'CONTROL_MODE_CHANGE'

# Special/synthetic message, sent when a controller reaches its maximum
# value. This is useful for treating these control inputs like a boolean
# value rather than a linear scale.
CONTROL_MODE_CHANGE_ON = 'CONTROL_MODE_CHANGE_ON'

# Default mapping, works great on / built on a Novation LaunchKey Mini
DEFAULT_MIDI_MAPPING = {
    # Corresponds to the track previous/next buttons
    (CONTROL_MODE_CHANGE_ON, 106): MidiFunctions.PLAYLIST_PREVIOUS,
    (CONTROL_MODE_CHANGE_ON, 107): MidiFunctions.PLAYLIST_NEXT,

    # Knob 1: BPM
    (CONTROL_MODE_CHANGE, 21): MidiFunctions.SET_BPM,

    # Pad 16
    (NOTE_ON, 'B2'): MidiFunctions.PLAYLIST_STAY,
}

class MidiHandler(pymidi_server.Handler):
    def __init__(self, manager):
        self.manager = manager

    def on_peer_connected(self, peer):
        self.manager.on_midi_peer_connected(peer)

    def on_peer_disconnected(self, peer):
        self.manager.on_midi_peer_disconnected(peer)

    def on_midi_commands(self, peer, commands):
        self.manager.on_midi_commands(peer, commands)


class MidiManager(object):
    """Binds a pymidi server to the dance floor controller."""
    def __init__(self, port, controller):
        self.controller = controller
        self.midi_server = pymidi_server.Server(port=port)
        self.midi_server.add_handler(MidiHandler(self))
        self.logger = logging.getLogger(self.__class__.__name__)
        self.peers = {}
        self.logger.info('Midi enabled, port={}'.format(port))

    def get_midi_mapping(self, peer):
        """Returns the midi mapping for this peer."""
        # TODO(mikey): Support customized mappings.
        return DEFAULT_MIDI_MAPPING

    def command_to_tuple(self, cmd):
        """Canonicalizes a midi message to function tuple(s).

        Function tuples are key portion of a midi mapping.

        For example, the MIDI message:
            'note_on C3 36'
        ... would become the tuple:
            ('NOTE_ON', 'C3')

        While usually only one value will be returned, control/mode change
        midi messages have two forms: one for use with its scalar value (useful
        for things like setting BPM), and one for use as a binary value (useful
        like a simple push button, for midi devices which map some buttons this way).

        For example,
            'control_mode_change' 22 127
        ... would become:
            ('CONTROL_MODE_CHANGE', 22)
            ('CONTROL_MODE_CHANGE_ON', 22)
        since 127 is the maximum value.
        """
        if cmd.command == 'note_on':
            yield (NOTE_ON, str(cmd.params.key))
        elif cmd.command == 'control_mode_change':
            yield (CONTROL_MODE_CHANGE, cmd.params.controller)
            if cmd.params.value == 127:
                yield (CONTROL_MODE_CHANGE_ON, cmd.params.controller)

    def on_midi_peer_connected(self, peer):
        self.logger.info('Peer connected: {}'.format(peer))
        self.peers[peer.ssrc] = peer

    def on_midi_peer_disconnected(self, peer):
        self.logger.info('Peer disconnected: {}'.format(peer))
        del self.peers[peer.ssrc]

    def on_midi_commands(self, peer, commands):
        mapping = self.get_midi_mapping(peer)
        for command in commands:
            keys = self.command_to_tuple(command)
            for key in keys:
                if key in mapping:
                    self.execute_midi_function(mapping[key], command)
                    handled = True
                else:
                    self.logger.info('Unhandled: {}'.format(key))

    def execute_midi_function(self, function_name, command):
        self.logger.info('MIDI function: {}'.format(function_name))
        playlist = self.controller.playlist

        if function_name == MidiFunctions.PLAYLIST_NEXT:
            if playlist:
                playlist.advance()
        elif function_name == MidiFunctions.PLAYLIST_PREVIOUS:
            if playlist:
                playlist.previous()
        elif function_name == MidiFunctions.PLAYLIST_STOP:
            if playlist:
                playlist.stop_playlist()
        elif function_name == MidiFunctions.PLAYLIST_PLAY:
            if playlist:
                playlist.start_playlist()
        elif function_name == MidiFunctions.PLAYLIST_STAY:
            if playlist:
                playlist.stay()
        elif function_name == MidiFunctions.SET_BPM:
            value = command.params.value
            bpm = 90
            bpm += float(value) / 127.0 * 80
            self.controller.set_bpm(bpm)

    def run_server(self):
        thr = threading.Thread(target=self.midi_server.serve_forever)
        thr.daemon = True
        self.logger.info('Starting midi server thread')
        thr.start()
