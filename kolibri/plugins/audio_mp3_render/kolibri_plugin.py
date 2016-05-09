# -*- coding: utf-8 -*-
"""
Copy and modify this code for your own plugin.
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from kolibri.plugins.base import KolibriFrontEndPluginBase
from kolibri.plugins.hooks import CONTENT_RENDERER_ASYNC

logger = logging.getLogger(__name__)


class KolibriAudioMP3RenderFrontEnd(KolibriFrontEndPluginBase):
    """
    The base learn code for the learn page.
    """
    entry_file = "assets/src/render_audio_mp3_module.js"

    events = {
        "content_render:audio/mp3": "render"
    }

    def hooks(self):
        return {
            CONTENT_RENDERER_ASYNC: self.plugin_name,
        }


PLUGINS = [
    KolibriAudioMP3RenderFrontEnd,
]