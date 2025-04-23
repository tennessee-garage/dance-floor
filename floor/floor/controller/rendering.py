from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from builtins import object, str

from floor.processor.constants import RANGED_INPUT_MAX


class BaseRenderLayer(object):
    """Abstract class for anything that can return a frame of pixels."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.enabled = True
        self.alpha = 1.0
        self.ranged_values = [0] * 4
        self.switches = [False] * 4

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

    def is_enabled(self):
        return self.enabled and self.alpha > 0

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = min(1.0, max(0, alpha))

    def on_ranged_value_change(self, num, val):
        """Sets the ranged input value.

        Arguments:
            num {integer} -- The 0-indexed fader/slider number, between 0-3 inclusive
            val {integer} -- The position value, between 0-`RANGED_INPUT_MAX` inclusive
        """
        val = max(0, min(val, RANGED_INPUT_MAX))
        self.logger.debug("on_ranged_value_change: {} -> {}".format(num, val))
        if num >= len(self.ranged_values):
            return
        self.ranged_values[num] = val

    def on_switch_change(self, num, is_on):
        """Sets the on/off switch value.

        Arguments:
            num {integer} -- The 0-indexed switch number, between 0-3 inclusive
            is_on {bool} -- Whether the switch should be on or off
        """
        is_on = bool(is_on)
        self.logger.debug("on_switch_change: {} -> {}".format(num, is_on))
        if num >= len(self.switches):
            return
        self.switches[num] = bool(is_on)

    def render(self, render_context):
        """Return a frame of pixels

        Arguments:
            render_context {RenderContext} -- The current rendering context.

        Returns:
            An iterable of pixels, or `None` if layer is disabled.
        """
        raise NotImplementedError


class ProcessorRenderLayer(BaseRenderLayer):
    """A RenderLayer that encapsulates a single Processor."""

    def __init__(self, processor=None):
        super(ProcessorRenderLayer, self).__init__()
        self.processor = processor

    def is_enabled(self):
        return self.processor is not None and self.enabled

    def on_ranged_value_change(self, num, val):
        """Extends the base implementation to add a callback to the current processor."""
        super(ProcessorRenderLayer, self).on_ranged_value_change(num, val)
        if self.processor:
            self.processor.on_ranged_value_change(num, val)

    def render(self, render_context):
        if self.processor:
            return self.processor.get_next_frame(render_context)
        return None

    def set_processor(self, processor):
        self.processor = processor

    def get_processor(self):
        return self.processor

    def get_processor_name(self):
        if not self.processor:
            return None
        return self.processor.__class__.__name__


class PlaylistRenderLayer(BaseRenderLayer):
    """A RenderLayer that encapsulates a Playlist."""

    def __init__(self, playlist_manager, all_processors):
        super(PlaylistRenderLayer, self).__init__()
        self.playlist_manager = playlist_manager
        self.all_processors = all_processors
        self.logger = logging.getLogger(__name__)

        self.current_playlist_item = None
        self.current_processor = None
        self.processor_render_layer = ProcessorRenderLayer()

    def set_enabled(self, enabled):
        """Suspend/unsuspend the playlist when the layer is enabled/disabled."""
        super(PlaylistRenderLayer, self).set_enabled(enabled)
        current_playlist = self.playlist_manager.get_current_playlist()
        if self.enabled and not current_playlist.is_running():
            current_playlist.start_playlist()
        elif not self.enabled and current_playlist.is_running():
            current_playlist.stop_playlist()

    def on_ranged_value_change(self, num, val):
        return self.processor_render_layer.on_ranged_value_change(num, val)

    def on_switch_change(self, num, is_on):
        return self.processor_render_layer.on_switch_change(num, is_on)

    def get_processor_name(self):
        return self.processor_render_layer.get_processor_name()

    def render(self, render_context):
        current_playlist = self.playlist_manager.get_current_playlist()
        if not current_playlist.is_running():
            return None
        self._check_playlist(current_playlist, render_context)
        try:
            return self.processor_render_layer.render(render_context)
        except KeyboardInterrupt:
            raise
        except Exception:
            self.logger.exception(
                "Error generating frame for processor {}".format(self.current_processor)
            )
            self.logger.warning("Removing processor due to error.")
            current_playlist.remove(current_playlist.position)
            return None

    def _check_playlist(self, playlist, render_context):
        item = playlist.get_current()
        if not item:
            return

        if item is not self.current_playlist_item:
            self.logger.debug("Loading playlist item {}".format(item))
            self._set_current_item(item)

    def _set_current_item(self, item):
        """Sets the active playlist item."""
        self.current_processor = self._build_processor(item)
        self.processor_render_layer.set_processor(self.current_processor)
        self.logger.info("Started processor '{}'".format(self.current_processor))
        self.current_playlist_item = item

    def _build_processor(self, item):
        """Builds a processor instance."""
        processor_cls = item.processor_cls
        processor_args = item.processor_args
        try:
            return processor_cls(**processor_args)
        except Exception as e:
            raise ValueError(
                'Processor "{}" could not be created: {}'.format(processor_cls, str(e))
            )
