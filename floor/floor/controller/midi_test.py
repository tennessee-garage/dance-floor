from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase

from floor.controller.midi.constants import *
from floor.controller.midi.functions import MidiFunctions
from floor.controller.midi.manager import MidiManager
from floor.controller.midi.mapping import MidiMapping

import mock


DEMO_MAPPING = MidiMapping(name='demo', mappings={
    (COMMAND_NOTE_ON, 'C3'): MidiFunctions.playlist_next,
    (COMMAND_NOTE_ON, 'C4'): MidiFunctions.playlist_previous,
    (COMMAND_CONTROL_MODE_CHANGE, 21, 127): MidiFunctions.playlist_stop,
})


class MidiMappingTestCase(TestCase):
    def setUp(self):
        self.mapping = DEMO_MAPPING

    def test_basic_mapping(self):
        match = self.mapping.get_function((COMMAND_NOTE_ON, 'C3'))
        self.assertEqual(MidiFunctions.playlist_next, match)

        match = self.mapping.get_function((COMMAND_NOTE_ON, 'C3', 101))
        self.assertEqual(MidiFunctions.playlist_next, match)

        match = self.mapping.get_function((COMMAND_NOTE_ON, 'C1'))
        self.assertEqual(None, match)

        match = self.mapping.get_function((COMMAND_CONTROL_MODE_CHANGE, 21, 127))
        self.assertEqual(MidiFunctions.playlist_stop, match)

        match = self.mapping.get_function((COMMAND_CONTROL_MODE_CHANGE, 21, 99))
        self.assertEqual(None, match)

    def test_to_from_json(self):
        clone = MidiMapping.from_json(self.mapping.to_json())
        self.assertEqual(clone, self.mapping)


class MidiManagerTestCase(TestCase):
    def setUp(self):
        self.controller = mock.Mock()
        self.controller.processor = mock.Mock()
        self.controller.processor.handle_midi_command = mock.Mock()
        self.mapping = DEMO_MAPPING
        self.manager = MidiManager(
            port=1234,
            controller=self.controller,
            default_midi_mapping=self.mapping)

    def inject_note_on(self, key, velocity):
        fake_command = mock.Mock()
        fake_command.command = 'note_on'
        fake_command.params.key = key
        fake_command.params.velocity = velocity
        return self.inject_midi_command(fake_command)

    def inject_control_mode_change(self, controller, value):
        fake_command = mock.Mock()
        fake_command.command = 'control_mode_change'
        fake_command.params.controller = controller
        fake_command.params.value = value
        return self.inject_midi_command(fake_command)

    def inject_midi_command(self, command):
        handler = self.manager.midi_handler
        peer = mock.Mock()
        peer.name = 'fake'
        peer.ssrc = 1234
        handler.on_midi_commands(peer, [command])

    def test_midi_passthru(self):
        self.assertEqual(0, self.controller.playlist.advance.call_count)
        self.inject_note_on('C3', 127)
        self.assertEqual(1, self.controller.playlist.advance.call_count)

        self.assertEqual(0, self.controller.playlist.previous.call_count)
        self.inject_note_on('C4', 55)
        self.assertEqual(1, self.controller.playlist.previous.call_count)

        self.assertEqual(0, self.controller.playlist.stop_playlist.call_count)
        self.inject_control_mode_change(21, 11)
        self.assertEqual(0, self.controller.playlist.stop_playlist.call_count)
        self.inject_control_mode_change(21, 127)
        self.assertEqual(1, self.controller.playlist.stop_playlist.call_count)

        self.assertEqual(4, self.controller.processor.handle_midi_command.call_count)
        self.controller.processor.handle_midi_command.assert_has_calls([
            mock.call(('note_on', 'C3', 127)),
            mock.call(('note_on', 'C4', 55)),
            mock.call(('control_mode_change', 21, 11)),
            mock.call(('control_mode_change', 21, 127)),
        ])

    def test_note_name_translation(self):
        self.inject_note_on('Csn1', 127)
        self.assertEqual(1, self.controller.processor.handle_midi_command.call_count)
        self.controller.processor.handle_midi_command.assert_called_once_with(
            ('note_on', 'C#-1', 127)
        )
