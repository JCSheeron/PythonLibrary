#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ClassName.py
#
# imports
#

class ClassName(object):
    # class constants
    # (none)

    # default ctor
    def __init__(self):
        pass

    # ctor with params
    def __init__(self, paramA, paramB):
        # _ prefix is a convention for private or something that should not
        # accessed outside the class. But the _name isn't enforced as private.
        # it is just considered a bad style violation to access it externally.
        self._paramA = paramA
        self._paramB = paramB
        pass

    def __repr__(self):
        # __repr__ should create a 'representation that
        # should look like a valid Python Expression that could be used
        # to recreate an object with the same value.'
        # The goal of __repr__ is to be unambiguous.
        # Implement __repr__ for any class you implement.
        pass

    def __str__(self):
        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        # Implement __str__ if you think it would be useful to have a string
        # version which errs on the side of readability in favor of more
        # ambiguity
        pass

    def MyMethod1(self):
        pass

    def MyMethod1(self, ParamA):
        pass

    def __nameMangled_method(self): # for mangling
        # double underscore names will mangle the name with the class name
        # to avoid conflicts of attribute names between classes
        pass

    # properties
    @property
    def ParamA(self):
        return self._paramA

    @ParamA.setter
    def ParamA(self, newValue):
        self._paramA = newValue
        pass

    @ParamA.deleter
    def ParamA(self):
        # note deleters may not always be needed
        del self._paramA
        pass
