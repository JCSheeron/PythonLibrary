#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# bpsList.py
# Funcitons for dealing with lists
#
# Break a list into n-size chunks, and return as a list of lists.
# If seq cannot be converted to a list, return None.
# If chuckSizse cannot be converted to an integer, return the original list.
def listChunk(seq, chunkSize):
    """Given a list, return a list of lists broken into the specified chunk size.

    If seq cannot be converted to a list, return an empty list.
    If chuckSizse cannot be converted to an integer, return the original list."""

    # Make sure sequence can be turned into a list. Message and out if not.
    try:
        srcList = list(seq)
    except ValueError as ve:
        print(
            "ERROR: The seq parameter of the listChuck function must be passed a list or something \
convertable to a list. No list to return."
        )
        print(ve)
        return list()

    try:
        n = int(chunkSize)
        if 0 >= n:
            raise ValueError
    except ValueError as ve:
        print(
            "ERROR: The listChunk parameter of the listChuck function must be passed an interger or something \
convertable to an integer, and must >= 0. Returning the original list."
        )
        print(ve)
        # return the original list
        return srcList
    # break the list into chucks using list comprehension
    # list = <output expression>  for i in <input sequence>
    # (len(srcList) + n -1 // n) will be the number of chunks needed. Range converts this to a zero
    # based sequence to be used as an index. For each index (i), slicing is used to create a chunk.
    return [srcList[i * n : (i + 1) * n] for i in range((len(srcList) + n - 1) // n)]


# Return a list of duplicate values
def listDuplicates(seq):
    """Given a list, return a list of duplicate values."""
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
    """Given two lists/sets, return a list of values found in both."""
    # Make sure listA and ListB can be a list/set. Message and out if not.
    try:
        srcSetA = set(seqA)
    except ValueError as ve:
        print(
            "ERROR: listToListIntersection function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 1st argument."
        )
        print(ve)
        return None
    try:
        srcSetB = set(seqB)
    except ValueError as ve:
        print(
            "ERROR: listToListIntersection function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 2nd argument."
        )
        print(ve)
        return None
    # return a list of common values.
    return list(set(srcSetA).intersection(srcSetB))


# Return a list of values found in A but not in B
def listANotInB(seqA, seqB):
    """Given two lists/sets, return a list of values found only in the first one."""
    # Make sure listA and ListB can be a set. Message and out if not.
    try:
        srcSetA = set(seqA)
    except ValueError as ve:
        print(
            "ERROR: listANotInB function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 1st argument."
        )
        print(ve)
        return None
    try:
        srcSetB = set(seqB)
    except ValueError as ve:
        print(
            "ERROR: listANotInB function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 2nd argument."
        )
        print(ve)
        return None
    # return a list of values that are not in the second sequence
    return list(filter(lambda ele: ele not in srcSetB, srcSetA))


# Return true if list A is a subset of list B
def listAisSubset(seqA, seqB):
    """Given two lists/sets, return true if the first is a subset of the second."""
    # Make sure listA and ListB can be a set. Message and out if not.
    try:
        srcSetA = set(seqA)
    except ValueError as ve:
        print(
            "ERROR: listAIsSubset function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 1st argument."
        )
        print(ve)
        return False
    try:
        srcSetB = set(seqB)
    except ValueError as ve:
        print(
            "ERROR: listAIsSubset function must be passed two list/set \
objects, or two obejcts that can be converted to sets.  This is not the case \
for the 2nd argument."
        )
        print(ve)
        return False
    # return true if set A is a subset of B
    return srcSetA.issubset(srcSetB)
