"""
This module is responsible for taking a panel name and constructing the
appropriate Panel object.
"""

from util import Point

from classes.Panel import ListPanel

def make_panel(name, dimensions):
    maker = get_maker(name)
    panel = maker(dimensions)

    return panel

def get_maker(name):
    if name == 'Previous Directory':
        return _make_previous_directory_panel
    elif name == 'Current Directory':
        return _make_current_directory_panel
    elif name == 'Tags':
        return _make_tags_panel
    else:
        raise ValueError(name)

def _make_previous_directory_panel(dimensions):
    panel_dimensions = get_vertical_third_dimensions(dimensions, 1)
    panel = ListPanel(panel_dimensions, "Previous Directory")

    return panel

def _make_current_directory_panel(dimensions):
    panel_dimensions = get_vertical_third_dimensions(dimensions, 2)
    panel = ListPanel(panel_dimensions, "Current Directory")

    return panel

def _make_tags_panel(dimensions):
    panel_dimensions = get_vertical_third_dimensions(dimensions, 3)
    panel = ListPanel(panel_dimensions, "Tags")

    return panel

def get_vertical_third_dimensions(dimensions, panel_num):
    (ul, lr) = dimensions
    third = round(lr.x / 3)
    panel_ul = Point(ul.y, third * (panel_num - 1))
    panel_lr = Point(lr.y, min(lr.x, third * panel_num))
    panel_dimensions = (panel_ul, panel_lr)

    return panel_dimensions
