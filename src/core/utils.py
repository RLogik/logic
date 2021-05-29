#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;
from typing import Union;
from yaml import load;
from yaml import FullLoader;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL VARIABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD readConfig
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def readConfig(path: str) -> dict:
    with open(path, 'r') as fp:
        spec = load(fp, Loader=FullLoader);
        if not isinstance(spec, dict):
            raise ValueError('Config is not a dictionary object!');
        return spec;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHOD getAttribute
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAttribute(obj: Any, *keys: Union[str, int]) -> Any:
    if len(keys) == 0:
        return obj;
    key = keys[0];
    try:
        if isinstance(key, str) and isinstance(obj, dict) and key in obj:
            return obj[key] if len(keys) == 0 else getAttribute(obj[key], *keys[1:]);
        elif isinstance(key, int) and isinstance(obj, (list,tuple)) and key < len(obj):
            return obj[key] if len(keys) == 0 else getAttribute(obj[key], *keys[1:]);
    except:
        pass;
    path = ' -> '.join([ key if isinstance(key, str) else '[{}]'.format(key) for key in keys ]);
    raise Exception('Could not find \033[1m{}\033[0m in object!'.format(path));
