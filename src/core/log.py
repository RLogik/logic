#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def logGeneric(tag: str, *lines: Any):
    for line in lines:
        print('{} {}'.format(tag, line));

def logInfo(*lines: Any):
    logGeneric('[\033[94;1mINFO\033[0m]', *lines);

def logDebug(*lines: Any):
    logGeneric('[\033[96;1mDEBUG\033[0m]', *lines);

def logWarn(*lines: Any):
    logGeneric('[\033[93;1mWARNING\033[0m]', *lines);

def logError(*lines: Any):
    logGeneric('[\033[91;1mERROR\033[0m]', *lines);

def logFatal(*lines: Any):
    logGeneric('[\033[94;1mFATAL\033[0m]', *lines);
    exit(1);
