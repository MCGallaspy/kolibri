# -*- coding: utf-8 -*-
"""
Kolibri template tags
=====================

To use

.. code-block:: html

    {% load kolibri_tags %}

    <ul>
    {% for navigation in kolibri_main_navigation %}
        <li><a href="{{ navigation.menu_url }}">{{ navigation.menu_name }}</a></li>
    {% endfor %}
    </ul>

"""
from __future__ import absolute_import, print_function, unicode_literals

from django import template

from kolibri.plugins import hooks

register = template.Library()


@register.assignment_tag()
def kolibri_main_navigation():

    for callback in hooks.get_callables(hooks.NAVIGATION_POPULATE):
        for item in callback():
            yield item
