# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import bytes, str
from gettext import gettext

from pyload.api import Input, InputType
from pyload.utils.convert import to_bool, to_str
from pyload.utils.lib.collections import namedtuple

ConfigData = namedtuple("ConfigData", "label description input")

# Maps old config formats to new values
input_dict = {
    "int": InputType.Int,
    "bool": InputType.Bool,
    "time": InputType.Time,
    "file": InputType.File,
    "list": InputType.List,
    "folder": InputType.Folder
}


def to_input(typ):
    """
    Converts old config format to input type.
    """
    return input_dict.get(typ, InputType.Text)


def to_configdata(entry):
    if len(entry) != 4:
        raise ValueError("Config entry must be of length 4")

    # Values can have different roles depending on the two config formats
    conf_name, type_label, label_desc, default_input = entry

    # name, label, desc, input
    if isinstance(default_input, Input):
        _input = default_input
        conf_label = type_label
        conf_desc = label_desc
    # name, type, label, default
    else:
        _input = Input(to_input(type_label))
        _input.default_value = from_string(default_input, _input.type)
        conf_label = label_desc
        conf_desc = ""

    return conf_name, ConfigData(
        gettext(conf_label), gettext(conf_desc), _input)


def from_string(value, typ=None):
    """
    Cast value to given type, unicode for strings.
    """

    # value is no string
    if not isinstance(value, str) and not isinstance(value, bytes):
        return value

    value = to_str(value)

    if typ == InputType.Int:
        return int(value)
    elif typ == InputType.Bool:
        return to_bool(value)
    elif typ == InputType.Time:
        if not value:
            value = "0:00"
        if not ":" in value:
            value += ":00"
        return value
    else:
        return value