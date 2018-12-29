class MidiFunctions(object):
    """Defines things that can be controlled over midi.

    Instances of this class are simple containers which contain the
    constant `.name` value. The name of a MidiFunction is stable value
    that may be used in a MidiMapping (see later).

    The `ALL_FUNCTIONS` global contains all registered/available functions
    in the system. You can think of it like an enum.
    """
    ALL_FUNCTIONS = {}

    def __init__(self, name, callback, help_text=''):
        self.name = name
        self.help_text = help_text
        self.callback = callback

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name, **kwargs):
        assert name not in cls.ALL_FUNCTIONS
        obj = cls(name, **kwargs)
        cls.ALL_FUNCTIONS[name] = obj
        setattr(cls, name, obj)


MidiFunctions.add('playlist_next',
                  callback=lambda controller, _: controller.playlist.advance(),
                  help_text='Advance to the next item in the current playlist.')
MidiFunctions.add('playlist_previous',
                  callback=lambda controller, _: controller.playlist.previous(),
                  help_text='Go to previous item in the current playlist.')
MidiFunctions.add('playlist_play',
                  callback=lambda controller, _: controller.playlist.play(),
                  help_text='Play the current playlist.')
MidiFunctions.add('playlist_stay',
                  callback=lambda controller, _: controller.playlist.stay(),
                  help_text='Loop/repeat the current item in the playlist.')
MidiFunctions.add('playlist_stop',
                  callback=lambda controller, _: controller.playlist.stop_playlist(),
                  help_text='Stop playback of the current playlist.')
MidiFunctions.add('playlist_goto_1',
                  callback=lambda controller, _: controller.playlist.go_to(1),
                  help_text='Go to playlist position 1.')
MidiFunctions.add('playlist_goto_2',
                  callback=lambda controller, _: controller.playlist.go_to(2),
                  help_text='Go to playlist position 2.')
MidiFunctions.add('playlist_goto_3',
                  callback=lambda controller, _: controller.playlist.go_to(3),
                  help_text='Go to playlist position 3.')
MidiFunctions.add('playlist_goto_4',
                  callback=lambda controller, _: controller.playlist.go_to(4),
                  help_text='Go to playlist position 4.')
MidiFunctions.add('playlist_goto_5',
                  callback=lambda controller, _: controller.playlist.go_to(5),
                  help_text='Go to playlist position 5.')
MidiFunctions.add('playlist_goto_6',
                  callback=lambda controller, _: controller.playlist.go_to(6),
                  help_text='Go to playlist position 6.')
MidiFunctions.add('playlist_goto_7',
                  callback=lambda controller, _: controller.playlist.go_to(7),
                  help_text='Go to playlist position 7.')
MidiFunctions.add('playlist_goto_8',
                  callback=lambda controller, _: controller.playlist.go_to(8),
                  help_text='Go to playlist position 8.')
MidiFunctions.add('playlist_goto_9',
                  callback=lambda controller, _: controller.playlist.go_to(9),
                  help_text='Go to playlist position 9.')
MidiFunctions.add('playlist_goto_10',
                  callback=lambda controller, _: controller.playlist.go_to(10),
                  help_text='Go to playlist position 10.')
MidiFunctions.add('playlist_goto_11',
                  callback=lambda controller, _: controller.playlist.go_to(11),
                  help_text='Go to playlist position 11.')
MidiFunctions.add('playlist_goto_12',
                  callback=lambda controller, _: controller.playlist.go_to(12),
                  help_text='Go to playlist position 12.')
MidiFunctions.add('playlist_goto_13',
                  callback=lambda controller, _: controller.playlist.go_to(13),
                  help_text='Go to playlist position 13.')
MidiFunctions.add('playlist_goto_14',
                  callback=lambda controller, _: controller.playlist.go_to(14),
                  help_text='Go to playlist position 14.')
MidiFunctions.add('playlist_goto_15',
                  callback=lambda controller, _: controller.playlist.go_to(15),
                  help_text='Go to playlist position 15.')
MidiFunctions.add('playlist_goto_16',
                  callback=lambda controller, _: controller.playlist.go_to(16),
                  help_text='Go to playlist position 16.')
MidiFunctions.add('set_bpm',
                  callback=lambda controller, value: controller.set_bpm(90 + 80 * (value/127.0)),
                  help_text='Set the global bpm based on note velocity or controller value.')
MidiFunctions.add('set_brightness',
                  callback=lambda controller, value: controller.scale_brightness(value/127.0),
                  help_text='Adjust the max brightness of the floor')

# Add a number of ranged values, likely faders or knobs, that can be used within processor code
# to tweak parameters.
for idx in range(0, 4):
    MidiFunctions.add('ranged_value_{}'.format(idx+1),
                      callback=lambda controller, value, i=idx: controller.handle_ranged_value(i, value),
                      help_text='A generic ranged value for adjusting processor parameters')

# Setup methods for floor foot presses
for idx in range(1, 65):
    MidiFunctions.add(
        'foot_on_square_{}'.format(idx),
        callback=lambda controller, _, i=idx: controller.square_weight_on(i),
        help_text='Send a foot step for square {}'.format(idx)
    )

# Setup methods for floor foot releases
for idx in range(1, 65):
    MidiFunctions.add(
        'foot_off_square_{}'.format(idx),
        callback=lambda controller, _, i=idx: controller.square_weight_off(i),
        help_text='Release a foot step for square {}'.format(idx)
    )
