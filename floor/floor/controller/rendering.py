from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging


class BaseRenderLayer(object):
    """Abstract class for anything that can return a frame of pixels."""

    def __init__(self):
        self.enabled = True

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

    def is_enabled(self):
        return self.enabled

    def on_ranged_value_change(self, num, val):
        pass

    def prepare(self):
        """Perform any setup prior to next call of `generate_frame`."""
        pass

    def render(self, render_context, leds):
        """Return a frame of pixels

        Arguments:
            render_context {RenderContext} -- The current rendering context.
            leds {list} -- The pixels rendered by previous layers, or None if
                           this is the first layter.

        Returns:
            An iterable of pixels.
        """
        raise NotImplementedError


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

    def on_ranged_value_change(self, num, val):
        if self.current_processor:
            self.current_processor.on_ranged_value_change(num, val)

    def render(self, render_context, leds):
        self._check_playlist(render_context)
        try:
            leds = self.current_processor.get_next_frame(render_context)
            return leds
        except KeyboardInterrupt:
            raise
        except Exception:
            self.logger.exception('Error generating frame for processor {}'.format(self.current_processor_name))
            self.logger.warning('Removing processor due to error.')
            self.playlist.remove(self.playlist.position)

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


class ProcessorRenderLayer(BaseRenderLayer):
    """A RenderLayer that encapsulates a single Processor."""
    def __init__(self, processor=None):
        super(ProcessorRenderLayer, self).__init__()
        self.processor = processor
        self.logger = logging.getLogger(__name__)

    def is_enabled(self):
        return self.processor is not None and self.is_enabled

    def on_ranged_value_change(self, num, val):
        if self.processor:
            self.processor.on_ranged_value_change(num, val)

    def render(self, render_context, leds):
        if self.processor:
            return self.processor.get_next_frame(render_context)
        return leds

    def set_processor(self, processor):
        self.processor = processor
