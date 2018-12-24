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
MidiFunctions.add('set_brightness',
                  help_text='Adjust the max brightness of the floor')

# Setup methods for floor foot presses
for idx in range(1, 65):
    MidiFunctions.add(
        'foot_on_square_{}'.format(idx),
        help_text='Send a foot step for square {}'.format(idx)
    )

# Setup methods for floor foot presses
for idx in range(1, 65):
    MidiFunctions.add(
        'foot_off_square_{}'.format(idx),
        help_text='Release a foot step for square {}'.format(idx)
    )
