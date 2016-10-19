#
# The BSD License (BSD)
#
# Copyright (c) 2016 Tintri, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#     without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__author__ = 'Tintri'
__copyright__ = 'Copyright 2016 Tintri Inc'
__license__ = 'BSD'
__version__ = '1.0'

import types
import json
import inspect
import logging
import pydoc
import re
import requests

DEFAULT_LOGGER_NAME = 'tintri'
# Precompile regexes for changing CamelCase to snake_case.
FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')

def map_to_object(m, cls):
    def __getobjecttype(cls, varname):
        from .__init__ import TintriObject
        if '_property_map' in dir(cls):
            if varname in cls._property_map.keys():
                return cls._property_map[varname]
        return TintriObject

    if type(m) == types.DictionaryType:
        o = cls()
        
        ignoresetattr = None
        if hasattr(o, '_ignoresetattr'):
            ignoresetattr = o._ignoresetattr
            o._ignoresetattr = True

        for k in m.keys():
            cls2 = __getobjecttype(cls, k)
            setattr(o, k, map_to_object(m[k], cls2))

        if ignoresetattr:
            o._ignoresetattr = ignoresetattr
            
        return o
    elif type(m) == types.ListType:
        objects = []
        for obj in m:
            objects.append(map_to_object(obj, cls))
        return objects
    else:
        return m

def get_plural_form(word):
    return word.endswith('s') or word.endswith('x') and '%ses' % word or '%ss' % word 

class TintriJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if o is None: return None
        else: return o.__dict__

#class TintriJSONEncoder(json.JSONEncoder):

def dump_object(obj, level=0, name='', logger=None):
    if logger is None:
        logger = logging.getLogger(DEFAULT_LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        # don't add a StreamHandler to the logger object if it already has one
        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            # Set the Formatter to the default format.
            ch.setFormatter(logging.Formatter())
            logger.addHandler(ch)

    #print " " * level + "[%s]:" % (type(obj).__name__)
    if level == 0:
        logger.info('[DUMP]',)
#         print " " * level + '>' * 14 + ' Object Dump ' + '>' * 14

    if obj == None:
        logger.info(" " * level + "%s[None]: None", name)
    elif type(obj) in [types.ListType, types.TupleType]:
        if len(obj) == 0:
            logger.info(" " * level + "%s[%s]: []", name, type(obj).__name__)
        else:
            logger.info(" " * level + "%s[%s]: [", name, type(obj).__name__)
            for e in obj:
                dump_object(e, level=level + 4, logger=logger)
            logger.info(" " * level + "]")
    elif hasattr(obj, '__dict__'):
        if len(obj.__dict__.keys()) == 0:
            logger.info(" " * level + "%s[%s]: {}", name, obj.__class__.__name__)
        else:
            logger.info(" " * level + "%s[%s]: {", name, obj.__class__.__name__)
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    dump_object(value, level=level + 4, name=key, logger=logger)
            logger.info(" " * level + "}")
    else:
        logger.info(" " * level + "%s[%s]: %s", name, type(obj).__name__, `obj`)

    #    if level == 0:
    #    print " " * level + '<' * 41

def object_to_json(obj):
    if obj == None:
        return None
    else:
        return json.dumps(obj.__dict__, cls=TintriJSONEncoder) # Use __dict__ to avoid not JSON serializable error

def getmethods(obj):
    return inspect.getmembers(obj, predicate=inspect.ismethod)

# TODO: Parameter decorator method.
def _parameter_handler(func): pass

def convert_to_snake_case(name):
    """
    Changes the inputed name from CamelCase to snake_case. The solution was taken from http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case.
    Args:

        name(str) - A string in CamelCase.
    Returns:
        str: - A string in snake_case.
    """
    s1 = FIRST_CAP_RE.sub(r'\1_\2', name)
    return ALL_CAP_RE.sub(r'\1_\2', s1).lower()

def convert_to_camel_case(name, capitalize_first_letter=True):
    new_name = "".join(item.title() for item in name.split('_'))
    if capitalize_first_letter:
        return new_name
    else:
        return new_name[0].lower() + new_name[1:]
