#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ClassName.py
#
# imports
#

class ClassName(object):
    """Single line summary description right under ClassName

    A more complete description after a blank line.
    Blah Blah Blah
    Blah Blah Blah
    Follow this with the closing of the quotes and a blank line.
    Last line of document."""

    # class constants
    CONST_NAME = 666

    # default ctor
    def __init__(self):
        """ Document ctor"""
        pass

    # ctor with params
    def __init__(self, paramA, paramB):
        """ Document ctor"""
        # _ prefix is a convention for private or something that should not
        # accessed outside the class. But the _name isn't enforced as private.
        # it is just considered a bad style violation to access it externally.
        self._paramA = paramA
        self._paramB = paramB
        pass

    def __repr__(self):
        """ Document fct"""

        # __repr__ should create a 'representation that
        # should look like a valid Python Expression that could be used
        # to recreate an object with the same value.'
        # The goal of __repr__ is to be unambiguous. This could be returning
        # a dictionary or list for example that captures the state of the
        # class.
        # Implement __repr__ for any class you implement.
        pass

    def __str__(self):
        """ Document fct"""

        # The goal of __str__ is to create a string representation
        # of the object that is readable to a user (not a programmer).
        # Implement __str__ if you think it would be useful to have a string
        # version which errs on the side of readability perhaps at the expense
        # of ambiguity
        pass

    def __double_method(self): # for mangling
        """ Document fct"""

        # double underscore names will mangle the name with the class name
        # to avoid conflicts of attribute names between classes
        pass

    # Getters and Setters and Deleters for ParamA
    # note the underscore to treat them as private.
    def _get_paramA(self):
        return self._paramA

    def _set_paramA(self, newValue):
        self._paramA = value

    def _del_radius(self):
        del self._paramA

    paramA = property(
            fget=_get_paramA,
            fset=_set_paramA,
            fdel=_del_radius,
            doc="The ParamA property."
            )

