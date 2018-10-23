#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsMath.py
# Math funcitons
#
from math import floor, ceil, log10
#
# Order of Magnatude (oom) ceiling
# Round value up to the next value with the same order of magnatude.
# If an order of magnatude is specified, it will be used, as long as it makes
# sense.  If it does not make sense, or if it not specified, the order 
# of magnitude of the value will be used. 
# Examples
# oomCeil(1805) returns 2000
# oomCeil(40050) returns 50000
# oomCeil(3521.7) returns 4000, oomCeil(3521.7, 3) returns 4000,
# oomCeil(3521.7, 2) returns 3600, oomCeil(3521.7, 1) returns 3530,
# and oomCeil(3521.7, 4) returns 10000 
def oomCeil(val, mag=None):
    '''Return value rounded up to the next value with the same or the specified order of magnitude.'''
    # Make sure sequence can be turned into an integer. Raise if not.
    try:
        value= ceil(val)
    except ValueError as ve:
        print('The value parmater must be convertable to an integer.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    oom=floor(log10(value))
    
    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int) and mag >= 0:
            oom=mag

    # Finally, caculate the oom ceiling
    multiple = 10**oom
    return ceil(value/multiple) * multiple

# Order of Magnatude (oom) floor
# Round value down to the nearest same order of magnatude value.
# If an order of magnatude is specified, it will be used, as long as it makes
# sense.  If it does not make sense, or if it not specified, the order 
# of magnitude of the value will be used. 
# Examples
# oomFloor(1805) returns 1000
# oomFloor(40050) returns 40000
# oomFloor(3521.7) returns 3000, oomFloor(3521.7, 3) returns 3000,
# oomFloor(3521.7, 2) returns 3500, oomFloor(3521.7, 1) returns 3520,
# oomFloor(3521.7, 4) returns 0, oomFloor(8521.7, 4) returns 0
def oomFloor(val, mag=None):
    '''Return value rounded up to the next value with the same or the specified order of magnitude.'''
    # Make sure sequence can be turned into an integer. Raise if not.
    try:
        value= floor(val)
    except ValueError as ve:
        print('The value parmater must be convertable to an integer.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    oom=floor(log10(value))
    
    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int) and mag >= 0:
            oom=mag

    # Finally, caculate the oom ceiling
    multiple = 10**oom
    return floor(value/multiple) * multiple

# Order of Magnatude (oom) round
# Round value to the nearest same order of magnatude value.
# If an order of magnatude is specified, it will be used, as long as it makes
# sense.  If it does not make sense, or if it not specified, the order 
# of magnitude of the value will be used. 
# Examples
# oomRound(1805) returns 2000
# oomRound(40050) returns 50000
# oomRound(3521.7) returns 4000, oomRound(3521.7, 3) returns 4000,
# oomRound(3521.7, 2) returns 3600, oomRound(3521.7, 1) returns 3530,
# and oomRound(3521.7, 4) returns 10000 
def oomRound(val, mag=None):
    '''Return value rounded up to the next value with the same or the specified order of magnitude.'''
    # Make sure sequence can be turned into an integer. Raise if not.
    try:
        value= round(val)
    except ValueError as ve:
        print('The value parmater must be convertable to an integer.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    oom=floor(log10(value))
    
    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int) and mag >= 0:
            oom=mag

    # Finally, caculate the oom ceiling
    multiple = 10**oom
    return round(value/multiple) * multiple


