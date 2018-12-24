from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import re
import threading

from pymidi import server as pymidi_server

from .functions import MidiFunctions
from .constants import COMMAND_NOTE_ON, COMMAND_NOTE_OFF, MIDI_NOTE_NAMES, COMMAND_CONTROL_MODE_CHANGE
from .mapping import MidiMapping


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
    def __init__(self, port, controller, default_midi_mapping=None):
        self.controller = controller
        self.midi_server = pymidi_server.Server(port=port)
        self.midi_handler = MidiHandler(self)
        self.midi_server.add_handler(self.midi_handler)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.midi_peers_to_mappings = {}
        self.logger.info('Midi enabled, port={}'.format(port))
        self.default_midi_mapping = default_midi_mapping or MidiMapping(name='default')

    def load_default_midi_mapping(self, mapping_dir, map_name):
        """Can be used to load a mapping JSON file to use as the default MIDI mapping"""

        mapping_file = mapping_dir + '/' + map_name + '.json'
        if os.path.isfile(mapping_file):
            try:
                self.default_midi_mapping = MidiMapping.from_file(mapping_file)
            except (KeyError, ValueError) as e:
                self.logger.error("Could not load mapping {}: {}".format(map_name, e))
            self.logger.info("Loaded MIDI mapping: {}".format(map_name))
        else:
            self.logger.error("Mapping file does not exist: {}".format(mapping_file))

    def get_midi_mapping(self, peer):
        """Returns the midi mapping for this peer."""
        return self.midi_peers_to_mappings.get(peer.ssrc, self.default_midi_mapping)

    @staticmethod
    def command_to_tuple(cmd):
        """Canonicalizes a pymidi command to its internal representation."""
        if cmd.command in (COMMAND_NOTE_ON, COMMAND_NOTE_OFF):
            command = cmd.command
            note_name = MIDI_NOTE_NAMES.get(cmd.params.key, cmd.params.key)
            value = cmd.params.velocity
            if command == COMMAND_NOTE_ON and value == 0:
                # MIDI protocol specifies note on with velocity zero as a logical
                # note off; make the translation here.
                command = COMMAND_NOTE_OFF
            return command, note_name, value
        elif cmd.command == COMMAND_CONTROL_MODE_CHANGE:
            return cmd.command, cmd.params.controller, cmd.params.value
        return None

    def on_midi_peer_connected(self, peer):
        self.logger.info('Peer connected: {}'.format(peer))
        self.midi_peers_to_mappings[peer.ssrc] = self.default_midi_mapping

    def on_midi_peer_disconnected(self, peer):
        self.logger.info('Peer disconnected: {}'.format(peer))
        del self.midi_peers_to_mappings[peer.ssrc]

    def on_midi_commands(self, peer, commands):
        commands = map(MidiManager.command_to_tuple, commands)

        # Pass all midi messages through to the current processor.
        processor = self.controller.processor
        if processor and hasattr(processor, 'handle_midi_command'):
            for command in commands:
                processor.handle_midi_command(command)

        logging.info("Key: {}".format(commands[0][1]))

        # Handle any special command bindings.
        mapping = self.get_midi_mapping(peer)
        for command in commands:
            func = mapping.get_function(command)
            if func:
                self.execute_midi_function(func, command)

    def execute_midi_function(self, midi_function, command):
        self.logger.info('MIDI function: {}'.format(midi_function))
        playlist = self.controller.playlist

        if midi_function == MidiFunctions.playlist_next:
            playlist.advance()
        elif midi_function == MidiFunctions.playlist_previous:
            playlist.previous()
        elif midi_function == MidiFunctions.playlist_stop:
            playlist.stop_playlist()
        elif midi_function == MidiFunctions.playlist_play:
            playlist.start_playlist()
        elif midi_function == MidiFunctions.playlist_stay:
            playlist.stay()
        elif midi_function == MidiFunctions.playlist_goto_1:
            playlist.go_to(1)
        elif midi_function == MidiFunctions.playlist_goto_2:
            playlist.go_to(2)
        elif midi_function == MidiFunctions.playlist_goto_3:
            playlist.go_to(3)
        elif midi_function == MidiFunctions.playlist_goto_4:
            playlist.go_to(4)
        elif midi_function == MidiFunctions.playlist_goto_5:
            playlist.go_to(5)
        elif midi_function == MidiFunctions.playlist_goto_6:
            playlist.go_to(6)
        elif midi_function == MidiFunctions.playlist_goto_7:
            playlist.go_to(7)
        elif midi_function == MidiFunctions.playlist_goto_8:
            playlist.go_to(8)
        elif midi_function == MidiFunctions.playlist_goto_9:
            playlist.go_to(9)
        elif midi_function == MidiFunctions.playlist_goto_10:
            playlist.go_to(10)
        elif midi_function == MidiFunctions.playlist_goto_11:
            playlist.go_to(11)
        elif midi_function == MidiFunctions.playlist_goto_12:
            playlist.go_to(12)
        elif midi_function == MidiFunctions.playlist_goto_13:
            playlist.go_to(13)
        elif midi_function == MidiFunctions.playlist_goto_14:
            playlist.go_to(14)
        elif midi_function == MidiFunctions.playlist_goto_15:
            playlist.go_to(15)
        elif midi_function == MidiFunctions.playlist_goto_16:
            playlist.go_to(16)
        elif midi_function == MidiFunctions.set_bpm:
            value = command[2]
            bpm = 90
            bpm += float(value) / 127.0 * 80
            self.controller.set_bpm(int(bpm))
        elif midi_function == MidiFunctions.set_brightness:
            value = command[2]
            self.controller.scale_brightness(value/127.0)
        elif midi_function.name in MidiFunctions.ALL_FUNCTIONS:
            # Look for a 'foot_on_square_1' type message.
            (state, num) = re.split('_square_',  midi_function.name)
            if state == 'foot_on':
                self.controller.square_weight_on(int(num)-1)
            elif state == 'foot_off':
                self.controller.square_weight_off(int(num)-1)

    def run_server(self):
        thr = threading.Thread(target=self.midi_server.serve_forever)
        thr.daemon = True
        self.logger.info('Starting midi server thread')
        thr.start()
