from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from floor.controller.playlist import Playlist
from floor.processor import all_processors
from unittest import TestCase

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_PLAYLIST = BASE_DIR + '/../../playlists/default.json'

class PlaylistTest(TestCase):
    def test_default_playlist(self):
        p = Playlist(filename=DEFAULT_PLAYLIST)
        self.assert_(len(p.queue) > 0, 'Expected non-zero default playlist.')

        all_procs = all_processors()
        for processor in p.queue:
            name = processor['name']
            if name not in all_procs:
                self.fail('Default playlist defines unknown processor "{}"'.format(name))
