from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from builtins import object
import logging

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
        self.logger.debug('on_ranged_value_change: {} -> {}'.format(num, val))
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
        self.logger.debug('on_switch_change: {} -> {}'.format(num, is_on))
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
    def __init__(self, playlist, all_processors):
        super(PlaylistRenderLayer, self).__init__()
        self.playlist = playlist
        self.all_processors = all_processors
        self.logger = logging.getLogger(__name__)

        self.current_processor = None
        self.current_processor_name = None
        self.current_processor_args = None
        self.processor_render_layer = ProcessorRenderLayer()

    def on_ranged_value_change(self, num, val):
        return self.processor_render_layer.on_ranged_value_change(num, val)

    def on_switch_change(self, num, is_on):
        return self.processor_render_layer.on_switch_change(num, is_on)

    def get_processor_name(self):
        return self.processor_render_layer.get_processor_name()

    def render(self, render_context):
        self._check_playlist(render_context)
        try:
            return self.processor_render_layer.render(render_context)
        except KeyboardInterrupt:
            raise
        except Exception:
            self.logger.exception('Error generating frame for processor {}'.format(self.current_processor_name))
            self.logger.warning('Removing processor due to error.')
            self.playlist.remove(self.playlist.position)
            return None

    def _check_playlist(self, render_context):
        item = self.playlist.get_current()
        if not item:
            return

        processor_name = item['name']
        args = item.get('args')
        if processor_name and (processor_name, args) != (self.current_processor_name, self.current_processor_args):
            self.logger.debug('Loading processor {}'.format(processor_name))
            self._set_processor(processor_name, args, render_context)

    def _set_processor(self, processor_name, processor_args, render_context):
        """Sets the active processor, which must already be loaded into
        `self.all_processors`.

        Raises `ValueError` if processor is unknown.
        """
        self.current_processor = self._build_processor(processor_name, processor_args)
        self.current_processor_name = processor_name
        self.current_processor_args = processor_args
        self.processor_render_layer.set_processor(self.current_processor)
        self.logger.info("Started processor '{}'".format(processor_name))

    def _build_processor(self, name, args=None):
        """Builds a processor instance."""
        args = args or {}
        processor_cls = self.all_processors.get(name)
        if not processor_cls:
            raise ValueError('Processor "{}" does not exist'.format(name))
        try:
            return processor_cls(**args)
        except Exception as e:
            raise ValueError('Processor "{}" could not be created: {}'.format(name, str(e)))
