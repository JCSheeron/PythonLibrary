#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsMath.py
# Math funcitons
#   oomCeil(val, mag=None)
#   oomFloor(val, mag=None)
#   oomRound(val, mag=None)
#   polyPrettyPrint(p, cdir=0, precision=8)
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
# Negative magnitude values are used for values between 0 and 1 or 0 and -1.
# oomCeil(0.0031) returns 1, but
# oomCeil(0.0031, -3) returns 0.004
# oomCeil(0.0031, -2) returns 0.01
# oomCeil(0.0031, -1) returns 0.1
# oomCeil(0.0031, -4) returns 0.0031, same for more negative values of mag.
def oomCeil(val, mag=None):
    '''Return value rounded up to the next value with the same or the specified order of magnitude.'''
    # Make sure val can be converted to a float.  Raise if not.
    try:
        value = float(val)
    except ValueError as ve:
        print('The value parmater must be a float, or convertable to a float.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    # Log of 0 is meaningless, so deal with this special case -- treat it
    # like a log of 1 (= 0). Use the absolute value so the oom reflects the
    # magnatude for negative values as well (log of a negative is an imaginary
    # number
    if val == 0:
        oom = 0
    else:
        oom=floor(log10(abs(value)))

    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int):
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
# Negative magnitude values are used for values between 0 and 1 or 0 and -1.
# oomFloor(0.0031) returns 0.003, but
# oomFloor(0.0031, -3) returns 0.003
# oomFloor(0.0031, -2) returns 0.0
# oomFloor(0.0031, -1) returns 0.0
# oomFloor(0.0031, -4) returns 0.0031, same for more negative values of mag.
def oomFloor(val, mag=None):
    '''Return value rounded down to the next value with the same or the specified order of magnitude.'''
    # Make sure val can be converted to a float.  Raise if not.
    try:
        value = float(val)
    except ValueError as ve:
        print('The value parmater must be a float, or convertable to a float.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    # Log of 0 is meaningless, so deal with this special case -- treat it
    # like a log of 1 (= 0). Use the absolute value so the oom reflects the
    # magnatude for negative values as well (log of a negative is an imaginary
    # number
    if val == 0:
        oom = 0
    else:
        oom=floor(log10(abs(value)))

    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int):
            oom=mag

    # Finally, caculate the oom floor
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
# Negative magnitude values are used for values between 0 and 1 or 0 and -1.
# oomRound(0.0067) returns 1, but
# oomRound(0.0067, -3) returns 0.007
# oomRound(0.0067, -2) returns 0.01
# oomRound(0.0067, -1) returns 0.0
# oomRound(0.0067, -4) returns 0.0067, same for more negative values of mag.
def oomRound(val, mag=None):
    '''Return value rounded up to the next value with the same or the specified order of magnitude.'''
    # Make sure val can be converted to a float.  Raise if not.
    try:
        value = float(val)
    except ValueError as ve:
        print('The value parmater must be a float, or convertable to a float.')
        print(ve)
        return None

    # Get the order of magnitude of value.  Do this before evaluating oom, so
    # that this can be used if oom is None or meaningless.
    # Log of 0 is meaningless, so deal with this special case -- treat it
    # like a log of 1 (= 0). Use the absolute value so the oom reflects the
    # magnatude for negative values as well (log of a negative is an imaginary
    # number
    if val == 0:
        oom = 0
    else:
        oom=floor(log10(abs(value)))

    # Use mag if it is specified, and makes sense.
    if mag is not None:
        if isinstance(mag, int):
            oom=mag

    # Finally, caculate the oom round
    multiple = 10**oom
    return round(value/multiple) * multiple



# Given an array of coefficients, p, return a nicely formatted
# polynomial string in the form:
#       anx^n + bn-1x^n-1 + ... + a1x + a0
# It removes trailing .0 if the coefficient is an integer,
# it only displays non-zero coefficients,
# and if a coefficient is 1, it is left off.
# By default, cdir=0, the coefficient array is assumed to be in order
# of decending power (highest power first). If direction <> 0, then
# the coefficient array is assumed to be in order of ascending power (lowest
# power first).
# The returned string will always print in decending power (highest order
# coefficients first).
# precision is used to control how may decimal places are included
def polyPrettyPrint(p, cdir=0, precision=8):
    '''Create a nicely formatted polynomial as a stirng'''
    # Make sure p is list-like
    try:
        coeffs= list(p)
        noCoeffs= len(coeffs) # how many coeffs
        res= '' # init so we can use +=, even the first time
    except ValueError as ve:
        print('The coefficients must be convertable to a list.')
        print(ve)
        return ''

    # make sure fix is int-like
    try:
        precision= int(precision)
        if precision < 0:
            precision= 0
    except ValueError as ve:
        print('The decimal precision parameter must be convertable to an integer.')
        print(ve)
        return ''

    # Reverse the list if direction is not default
    if cdir != 0:
        coeffs.reverse()

    # go thru to coeffs, and create the string
    for i, coeff in enumerate(coeffs, 1): # start at 1
        # remove trailing .0
        if int(coeff) == coeff:
            coeff = int(coeff)

        exp=noCoeffs - i # the exponent
        if exp > 1: # not x^1 or x^0
            if coeff == 1: # don't display coeff when = 1
                res += 'x^{e} + '.format(e=exp)
            elif coeff != 0:
                res += '{c:{width}.{precision}{type}}x^{e} + '.format(c=coeff, width=3, precision=precision, type='G' , e=exp)
        elif exp == 1:  # x^1 case
            if coeff == 1: # don't display coeff when = 1
                res += 'x + '
            elif coeff != 0:
                res += '{c:{width}.{precision}{type}}x + '.format(c=coeff, width=3, precision=precision, type='G')
        else:   # x^0 case
            if coeff != 0:  # nothing to do if coff is zero
                res += '{c:{width}.{precision}{type}} + '.format(c=coeff, width=3, precision=precision, type='G')
    # it could be the empty case, but if not, ditch the last ' + '
    if res:
        return res[:-3]
    else:
        return ''

