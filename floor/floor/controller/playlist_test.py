from __future__ import absolute_import, division, print_function, unicode_literals

import os
from unittest import TestCase

from floor.controller.playlist import Playlist, PlaylistItem, ProcessorNotFound
from floor.processor import all_processors

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_PLAYLIST = BASE_DIR + "/../../config/playlists/default.json"


class PlaylistTest(TestCase):
    def setUp(self):
        self.all_procs = all_processors()

    def test_default_playlist(self):
        p = Playlist.from_file(DEFAULT_PLAYLIST, self.all_procs, strict=True)
        self.assert_(len(p.queue) > 0, "Expected non-zero default playlist.")

    def test_playlist_item_from_and_to_object(self):
        item = PlaylistItem.from_object(
            {
                "name": "Animator",
            },
            self.all_procs,
        )

        item_object = item.to_object()
        self.assertEqual(
            {
                "name": "Animator",
                "title": "Animator",
                "args": {},
                "duration": None,
            },
            item_object,
        )

        item = PlaylistItem.from_object(
            {
                "name": "Animator",
                "title": "My Other Animator",
                "args": {"foo": "bar"},
                "duration": 123,
            },
            self.all_procs,
        )

        item_object = item.to_object()
        self.assertEqual(
            {
                "name": "Animator",
                "title": "My Other Animator",
                "args": {"foo": "bar"},
                "duration": 123,
            },
            item_object,
        )

    def test_playlist_item_invalid_processor_name(self):
        with self.assertRaises(ProcessorNotFound):
            PlaylistItem.from_object(
                {
                    "name": "ZoopZap",
                },
                self.all_procs,
            )
