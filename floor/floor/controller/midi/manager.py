from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import threading

from pymidi import server as pymidi_server

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
        self.midi_server = pymidi_server.Server([('0.0.0.0', port)])
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
        mapping = self.get_midi_mapping(peer)

        # Handle any MIDI command bindings.
        for command in commands:
            func = mapping.get_function(command)
            if not func:
                self.logger.info("Received unmapped command: {} {}".format(command[0], command[1]))
                continue

            value = command[2]

            try:
                func.callback(self.controller, value)
            except Exception:
                self.logger.exception('Error in MIDI command callback')

    def run_server(self):
        thr = threading.Thread(target=self.midi_server.serve_forever)
        thr.daemon = True
        self.logger.info('Starting midi server thread')
        thr.start()
