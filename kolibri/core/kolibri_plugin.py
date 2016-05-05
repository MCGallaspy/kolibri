"""
The core app of Kolibri also uses the plugin API <3
"""
from __future__ import absolute_import, print_function, unicode_literals

from kolibri.plugins.base import KolibriFrontEndPluginBase
from kolibri.plugins.hooks import FRONTEND_PLUGINS


class KolibriCoreFrontEnd(KolibriFrontEndPluginBase):
    """
    Plugin to handle
    """
    entry_file = "assets/src/kolibri_core_app.js"
    external = True
    core = True

    def hooks(self):
        return {
            FRONTEND_PLUGINS: self._register_front_end_plugins
        }


PLUGINS = (
    KolibriCoreFrontEnd,
)
