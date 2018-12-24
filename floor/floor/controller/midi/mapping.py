import json

from .functions import MidiFunctions
from .constants import SUPPORTED_COMMANDS


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
        for command, func in self.mappings.iteritems():
            mappings_list.append({
                'command': command,
                'function': func.name,
            })
        return {
            'name': self.name,
            'mappings': mappings_list,
        }

    @classmethod
    def from_file(cls, input_filename):
        """Load midi key to function mapping from JSON."""
        with open(input_filename) as json_data:
            json_obj = json.load(json_data)

        return cls.from_json(json_obj)

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
            func = MidiFunctions.ALL_FUNCTIONS.get(item['function'])
            if not func:
                continue
            mapping_dict[tuple(command)] = func
        return cls(name, mapping_dict)
