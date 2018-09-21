from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import threading
from pymidi import server as pymidi_server

# Maps pymidi note identifiers to their more conventional names.
MIDI_NOTE_NAMES = {
    'Cn1': 'C-1',
    'Csn1': 'C#-1',
    'Dn1': 'D-1',
    'Dsn1': 'D#-1',
    'En1': 'E-1',
    'Fn1': 'F-1',
    'Fsn1': 'F#-1',
    'Gn1': 'G-1',
    'Gsn1': 'G#-1',
    'An1': 'A-1',
    'Asn1': 'A#-1',
    'Bn1': 'B-1',
    'C0': 'C0',
    'Cs0': 'C#0',
    'D0': 'D0',
    'Ds0': 'D#0',
    'E0': 'E0',
    'F0': 'F0',
    'Fs0': 'F#0',
    'G0': 'G0',
    'Gs0': 'G#0',
    'A0': 'A0',
    'As0': 'A#0',
    'B0': 'B0',
    'C1': 'C1',
    'Cs1': 'C#1',
    'D1': 'D1',
    'Ds1': 'D#1',
    'E1': 'E1',
    'F1': 'F1',
    'Fs1': 'F#1',
    'G1': 'G1',
    'Gs1': 'G#1',
    'A1': 'A1',
    'As1': 'A#1',
    'B1': 'B1',
    'C2': 'C2',
    'Cs2': 'C#2',
    'D2': 'D2',
    'Ds2': 'D#2',
    'E2': 'E2',
    'F2': 'F2',
    'Fs2': 'F#2',
    'G2': 'G2',
    'Gs2': 'G#2',
    'A2': 'A2',
    'As2': 'A#2',
    'B2': 'B2',
    'C3': 'C3',
    'Cs3': 'C#3',
    'D3': 'D3',
    'Ds3': 'D#3',
    'E3': 'E3',
    'F3': 'F3',
    'Fs3': 'F#3',
    'G3': 'G3',
    'Gs3': 'G#3',
    'A3': 'A3',
    'As3': 'A#3',
    'B3': 'B3',
    'C4': 'C4',
    'Cs4': 'C#4',
    'D4': 'D4',
    'Ds4': 'D#4',
    'E4': 'E4',
    'F4': 'F4',
    'Fs4': 'F#4',
    'G4': 'G4',
    'Gs4': 'G#4',
    'A4': 'A4',
    'As4': 'A#4',
    'B4': 'B4',
    'C5': 'C5',
    'Cs5': 'C#5',
    'D5': 'D5',
    'Ds5': 'D#5',
    'E5': 'E5',
    'F5': 'F5',
    'Fs5': 'F#5',
    'G5': 'G5',
    'Gs5': 'G#5',
    'A5': 'A5',
    'As5': 'A#5',
    'B5': 'B5',
    'C6': 'C6',
    'Cs6': 'C#6',
    'D6': 'D6',
    'Ds6': 'D#6',
    'E6': 'E6',
    'F6': 'F6',
    'Fs6': 'F#6',
    'G6': 'G6',
    'Gs6': 'G#6',
    'A6': 'A6',
    'As6': 'A#6',
    'B6': 'B6',
    'C7': 'C7',
    'Cs7': 'C#7',
    'D7': 'D7',
    'Ds7': 'D#7',
    'E7': 'E7',
    'F7': 'F7',
    'Fs7': 'F#7',
    'G7': 'G7',
    'Gs7': 'G#7',
    'A7': 'A7',
    'As7': 'A#7',
    'B7': 'B7',
    'C8': 'C8',
    'Cs8': 'C#8',
    'D8': 'D8',
    'Ds8': 'D#8',
    'E8': 'E8',
    'F8': 'F8',
    'Fs8': 'F#8',
    'G8': 'G8',
    'Gs8': 'G#8',
    'A8': 'A8',
    'As8': 'A#8',
    'B8': 'B8',
    'C9': 'C9',
    'Cs9': 'C#9',
    'D9': 'D9',
    'Ds9': 'D#9',
    'E9': 'E9',
    'F9': 'F9',
    'Fs9': 'F#9',
    'G9': 'G9',
}

# Convenience aliases for pymidi commands
COMMAND_NOTE_ON = 'note_on'
COMMAND_NOTE_OFF = 'note_off'
COMMAND_CONTROL_MODE_CHANGE = 'control_mode_change'
SUPPORTED_COMMANDS = (COMMAND_NOTE_ON, COMMAND_NOTE_OFF, COMMAND_CONTROL_MODE_CHANGE)


class MidiFunctions(object):
    """Defines things that can be controlled over midi.

    Instances of this class are simple containers which contain the
    constant `.name` value. The name of a MidiFunction is stable value
    that may be used in a MidiMapping (see later).

    The `ALL_FUNCTIONS` global contains all registered/available functions
    in the system. You can think of it like an enum.
    """
    ALL_FUNCTIONS = {}

    def __init__(self, name, help_text=''):
        self.name = name
        self.help_text = help_text

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name, **kwargs):
        assert name not in cls.ALL_FUNCTIONS
        obj = cls(name, **kwargs)
        cls.ALL_FUNCTIONS[name] = obj
        setattr(cls, name, obj)


MidiFunctions.add('playlist_next',
    help_text='Advance to the next item in the current playlist.')
MidiFunctions.add('playlist_previous',
    help_text='Go to previous item in the current playlist.')
MidiFunctions.add('playlist_pause',
    help_text='Pause the current playlist.')
MidiFunctions.add('playlist_play',
    help_text='Pause the current playlist.')
MidiFunctions.add('playlist_stay',
    help_text='Loop/repeat the current item in the playlist.')
MidiFunctions.add('playlist_stop',
    help_text='Stop playback of the current playlist.')
MidiFunctions.add('playlist_goto_1',
    help_text='Go to playlist position 1.')
MidiFunctions.add('playlist_goto_2',
    help_text='Go to playlist position 2.')
MidiFunctions.add('playlist_goto_3',
    help_text='Go to playlist position 3.')
MidiFunctions.add('playlist_goto_4',
    help_text='Go to playlist position 4.')
MidiFunctions.add('playlist_goto_5',
    help_text='Go to playlist position 5.')
MidiFunctions.add('playlist_goto_6',
    help_text='Go to playlist position 6.')
MidiFunctions.add('playlist_goto_7',
    help_text='Go to playlist position 7.')
MidiFunctions.add('playlist_goto_8',
    help_text='Go to playlist position 8.')
MidiFunctions.add('playlist_goto_9',
    help_text='Go to playlist position 9.')
MidiFunctions.add('playlist_goto_10',
    help_text='Go to playlist position 10.')
MidiFunctions.add('playlist_goto_11',
    help_text='Go to playlist position 11.')
MidiFunctions.add('playlist_goto_12',
    help_text='Go to playlist position 12.')
MidiFunctions.add('playlist_goto_13',
    help_text='Go to playlist position 13.')
MidiFunctions.add('playlist_goto_14',
    help_text='Go to playlist position 14.')
MidiFunctions.add('playlist_goto_15',
    help_text='Go to playlist position 15.')
MidiFunctions.add('playlist_goto_16',
    help_text='Go to playlist position 16.')
MidiFunctions.add('set_bpm',
    help_text='Set the global bpm based on note velocity or controller value.')


class MidiMapping(object):
    """Maps MIDI commands to a special functions.

    Mappings will typically be one-to-one with MIDI devices, because the layout
    and configuration of physical keys and control surfaces varies widely.

    The internal representation is a map, from 2- or 3-tuple command, to desired
    MidiFunction instance. 2-tuple commands will match any velocity or value;
    3-tuple commands only match the specified velocity or value.

    Example internal representation:
        {
            ('note_on', 'C3'): MidiFunctions('playlist_next'),
            ('note_on', 'C4'): MidiFunctions('playlist_previous'),
            ('control_mode_change', 22, 127): MidiFunctions('set_bpm'),
        }

    Equivalent JSON representation:
        {
            "name": "KontrolPad",
            "mappings": [
                {
                    "command": ["note_on", "C3"],
                    "function": "playlist_next"
                },
                {
                    "command": ["note_on", "C4"],
                    "function": "playlist_previous"
                },
                {
                    "command": ["control_mode_change", 22, 127],
                    "function": "set_bpm"
                }
            ]
        }
    """
    def __init__(self, name, mappings=None):
        self.name = name
        self.mappings = mappings or {}

    def __eq__(self, other):
        if not isinstance(other, MidiMapping):
            return False
        return (self.name, self.mappings) == (other.name, other.mappings)

    def get_function(self, command):
        # Try an exact match (with velocity/value) first.
        exact_match = self.mappings.get(command)
        if exact_match or len(command) < 3:
            return exact_match

        # Try a partial match (ignore velocity/value).
        match = self.mappings.get(command[:2])
        return match

    def to_json(self):
        mappings_list = []
        for command, function in self.mappings.iteritems():
            mappings_list.append({
                'command': command,
                'function': function.name,
            })
        return {
            'name': self.name,
            'mappings': mappings_list,
        }

    @classmethod
    def from_json(cls, obj):
        """Creates an instance from a parsed JSON object.

        Entries for unknown commands or unknown functions will be ignored.
        Structural errors will throw a KeyError.
        """
        name = obj['name']
        mapping_list = obj['mappings']
        mapping_dict = {}
        for item in mapping_list:
            command = item['command']
            if command[0] not in SUPPORTED_COMMANDS:
                continue
            function = MidiFunctions.ALL_FUNCTIONS.get(item['function'])
            if not function:
                continue
            mapping_dict[tuple(command)] = function
        return cls(name, mapping_dict)


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

    def get_midi_mapping(self, peer):
        """Returns the midi mapping for this peer."""
        return self.midi_peers_to_mappings.get(peer.ssrc, self.default_midi_mapping)

    def command_to_tuple(self, cmd):
        """Canonicalizes a pymidi command to its internal representation."""
        if cmd.command in (COMMAND_NOTE_ON, COMMAND_NOTE_OFF):
            command = cmd.command
            note_name = MIDI_NOTE_NAMES.get(cmd.params.key, cmd.params.key)
            value = cmd.params.velocity
            if command == COMMAND_NOTE_ON and value == 0:
                # MIDI protocol specifies note on with velocity zero as a logical
                # note off; make the translation here.
                command = COMMAND_NOTE_OFF
            return (command, note_name, value)
        elif cmd.command == COMMAND_CONTROL_MODE_CHANGE:
            return (cmd.command, cmd.params.controller, cmd.params.value)
        return None

    def on_midi_peer_connected(self, peer):
        self.logger.info('Peer connected: {}'.format(peer))
        self.midi_peers_to_mappings[peer.ssrc] = self.default_midi_mapping

    def on_midi_peer_disconnected(self, peer):
        self.logger.info('Peer disconnected: {}'.format(peer))
        del self.midi_peers_to_mappings[peer.ssrc]

    def on_midi_commands(self, peer, commands):
        commands = map(self.command_to_tuple, commands)

        # Pass all midi messages through to the current processor.
        processor = self.controller.processor
        if processor and hasattr(processor, 'handle_midi_command'):
            for command in commands:
                processor.handle_midi_command(command)

        # Handle any special command bindings.
        mapping = self.get_midi_mapping(peer)
        for command in commands:
            function = mapping.get_function(command)
            if function:
                self.execute_midi_function(function, command)

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
            value = command.params.value
            bpm = 90
            bpm += float(value) / 127.0 * 80
            self.controller.set_bpm(bpm)

    def run_server(self):
        thr = threading.Thread(target=self.midi_server.serve_forever)
        thr.daemon = True
        self.logger.info('Starting midi server thread')
        thr.start()
