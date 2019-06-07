#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsString.py
# Handy string related functions
#
#   trimPrefix -- Given a string and a prefix, return the string
#   with the prefix trimmed off. If the prefix is not found, return
#   the original string.
#
def trimPrefix(longString, prefix):
    '''Trim prefix off a string and return the resulting string.'''
    # Make sure longString and prefix contain somehting
    try:
        lString = str(longString)
    except ValueError as ve:
        print('The sepcified string must be convertable to a string.')
        print(ve)
        return None

    try:
        pfix = str(prefix)
    except ValueError as ve:
        print('The sepcified prefix must be convertable to a string.')
        print(ve)
        return None

    if lString == '' or lString is None:
        return lString

    if pfix is None:
        return lString

    # if we get here, string and prefix are strings with something in them.  Assume
    # they are valid and use them.
    if lString.startswith(pfix):
        return lString[len(pfix):]
    return lString  # return original string if prefix is not found.

#   trimSuffix -- Given a string and a suffix, return the string
#   with the suffix trimmed off. If the suffix is not found, return
#   the original string.
#
def trimSuffix(longString, suffix):
    '''Trim suffix off a string and return the resulting string.'''
    # Make sure longString and suffix contain somehting
    try:
        lString = str(longString)
    except ValueError as ve:
        print('The sepcified string must be convertable to a string.')
        print(ve)
        return None

    try:
        sfix = str(suffix)
    except ValueError as ve:
        print('The sepcified suffix must be convertable to a string.')
        print(ve)
        return None

    if lString == '' or lString is None:
        return lString

    if sfix is None:
        return lString

    # if we get here, string, prefix, and suffix are strings with something in them.
    # Assume they are valid and use them.
    if lString.endswith(sfix):
        return lString[:-1 * len(sfix)]
    return lString  # return original string if suffix is not found.


#   trimPrefixSuffix -- Given a string, a prefix, and a suffix, return the string
#   with the prefix and suffix trimmed off. If the prefix or suffix is not found,
#   don't trim that part.
#
def trimPrefixSuffix(longString, prefix, suffix):
    '''Trim prefix and suffix off a string and return the resulting string.'''
    # Make sure longString prefix and suffix contain somehting
    try:
        lString = str(longString)
    except ValueError as ve:
        print('The sepcified string must be convertable to a string.')
        print(ve)
        return None

    try:
        pfix = str(prefix)
    except ValueError as ve:
        print('The sepcified prefix must be convertable to a string.')
        print(ve)
        return None

    try:
        sfix = str(suffix)
    except ValueError as ve:
        print('The sepcified suffix must be convertable to a string.')
        print(ve)
        return None

    if lString == '' or lString is None:
        return lStirng

    if pfix is None and sfix is None:
        return lString

    # if we get here, string and suffix are strings with something in them.  Assume
    # they are valid and use them.
    return(trimSuffix(trimPrefix(lString, pfix), sfix))


