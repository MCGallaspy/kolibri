"""
Kolibri configuration data
==========================

.. warning::
    Do not load any django.conf.settings stuff here. This configuration data
    precedes loading of settings, it is not part of the settings stack.

TODO: We need to figure out our conf API. Do we store in ini/json/yaml?

 * How do we retrieve config data?
 * When should configuration files be loaded and written?

This module should be easier to document, for instance by having VARIABLES
instead of a dict.

"""
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import os

logger = logging.getLogger(__name__)

KOLIBRI_HOME = os.environ["KOLIBRI_HOME"]

# Creating KOLIBRI_HOME atm. has to happen here as for instance utils.cli is not
# called through py.test. This file is the first basic entry point of
# Kolibri, although utils.cli may or may not precede it.
if not os.path.exists(KOLIBRI_HOME):
    parent = os.path.dirname(KOLIBRI_HOME)
    if not os.path.exists(parent):
        raise RuntimeError("The parent of your KOLIBRI_HOME does not exist: {}".format(parent))
    os.mkdir(KOLIBRI_HOME)

conf_file = os.path.join(KOLIBRI_HOME, "kolibri_settings.json")

if not os.path.isfile(conf_file):
    logger.info("Writing default config file in {}".format(conf_file))
    open(conf_file, "w").write("{}")

#: Set defaults before updating the dict
config = {}

#: Everything in this list is added to django.conf.settings.INSTALLED_APPS
config['INSTALLED_APPS'] = []

#: Well-known plugin names that are automatically searched for and enabled on
#: first-run.
config['AUTO_SEARCH_PLUGINS'] = ['some.plugin.module.path']

#: If a config file does not exist, we assume it's the first run
config['FIRST_RUN'] = True

# Open up the config file and overwrite defaults
with open(conf_file, 'r') as kolibri_conf_file:
    config.update(json.load(kolibri_conf_file))

def save(first_run=False):
    """Saves the current state of the configuration"""
    config['FIRST_RUN'] = first_run
    with open(conf_file, 'w') as kolibri_conf_file:
        json.dump(config, kolibri_conf_file)
