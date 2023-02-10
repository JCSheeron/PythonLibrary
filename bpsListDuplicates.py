#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsListDuplicates.py
# Funcitons for dealing with duplicate values in lists
# NOTE: DEPRECATED!!!
# Use bpsList library instead. This file in kept for backward compatability, but
# new functions and changes are not added. The bpsList library includes the original
# listDuplicates and listToListIntersection funcitons, but also includes others.
#
# Return a list of duplicate values
def listDuplicates(seq):
    # Make sure sequence can be turned into a list. Message and out if not.
    try:
        srcList = list(seq)
    except ValueError as ve:
        print(
            "ERROR: listDuplicates function must be passed a list or something \
convertable to a list."
        )
        print(ve)
        return None

    seen = set()
    # use variable as a function below
    seen_add = seen.add
    # adds all elements not yet known to seen, and all others to seen_twice
    seen_twice = set(x for x in srcList if x in seen or seen_add(x))
    # covert to a set and return
    return list(seen_twice)


# Return a list of values found in both lists
def listToListIntersection(seqA, seqB):
    # Make sure listA and ListB can be a list. Message and out if not.
    try:
        srcListA = list(seqA)
    except ValueError as ve:
        print(
            "ERROR: listToListIntersection function must be passed two list \
objects, or two obejcts that can be converted to lists.  This is not the case \
for the 1st argument."
        )
        print(ve)
        return None
    try:
        srcListB = list(seqB)
    except ValueError as ve:
        print(
            "ERROR: listToListIntersection function must be passed two list \
objects, or two obejcts that can be converted to lists.  This is not the case \
for the 2nd argument."
        )
        print(ve)
        return None
    # return a list of common values.
    return list(set(srcListA).intersection(srcListB))
