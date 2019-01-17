#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pyTemplate.py
#
# This is intended to be a template to be used as a starting place when creating a
# new python program. It is just a basic formatted framwork and some examples of
# how to set up command line arguments.
#
# Command line arguments are:
# inputFileName (required, positional). The source data csv file.
#
# outputFileName (required, positional). The .csv output file name.
#
# -t, (required and mutually exclusive with -a and -n).  Input file
# is a historical trend export file.  The format is:
#     Tag1 TimeStamp, Tag1 Value, Tag2 TimeStamp, Tag2Timestamp ...
#
# -a (required and mutually exclusive with -t and -n). Input file is a
# archive export file. The format is:
#     TagId, TagName, Timestamp (YYYY-MM-DD HH:MM:SS.mmm), DataSource, Value, Quality
#
# -n (required and mutually exclusive with -t and -a). Input file is a time
# normalized export file.  The format is:
#     Timestamp, Time Bias, Tag1 Value, Tag2 Value, Tag3 Value ...
#
# -am1, -am2, -am3, -am4 or --archiveMergen (optional, default=None). Archive Merge.
# Merge these named files with the data in the inputFileName before processing.
# Must have the same format/layout as the input file.
#
# imports
#
# system related
# import sys
# date and time stuff
from datetime import datetime, time
# from pandas.tseries.frequencies import to_offset
# from dateutil import parser as duparser

# csv file stuff
# import csv

# arg parser
import argparse

# numerical manipulation libraries
# import numpy as np
# import pandas as pd

# user libraries
# Note: May need PYTHONPATH (set in ~/.profile?) to be set depending
# on the location of the imported files
# TimeStamped Indexed Data Class
# from bpsTsIdxData import TsIdxData
# list duplication helper functions
# from bpsListDuplicates import listDuplicates 
# from bpsListDuplicates import listToListIntersection


# **** argument parsing
# define the arguments
# create an epilog string to further describe the input file
eplStr="""Python Program Template file
 This can be a very long string that describes the program, the command 
 line arguments, options, etc. """

descrStr="Short description string."
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                                 description=descrStr, epilog=eplStr)
parser.add_argument('posArg1', help='Positional Argument 1')
parser.add_argument('posArg2', help= 'Positional Argument 2')
parser.add_argument('-optArg1', '--optionalArgument1', default=None, metavar='', \
                   help='Optional Argument 1')
parser.add_argument('-optArg2', '--optionalArgument2', default='default2', metavar='', \
                   help='Optional Argument 2. How to escape a special \
character (\", \").How to escape the %% character.')
parser.add_argument('-optTFArg1', action='store_true', default=False, \
                    help='True/False argument set to default to False, and is \
set to True if the argument is specified. The argument takes no values.')
# add a mutually exclusive required group
typegroup = parser.add_mutually_exclusive_group(required=True)
typegroup.add_argument('-me1',  action='store_true', default=False, \
                    help='Mutually Exclusive choice 1')
typegroup.add_argument('-me2', action='store_true', default=False, \
                    help='Mutually Exclusive choice 2')
typegroup.add_argument('-me3', action='store_true', default=False, \
                    help='Mutually Exclusive choice 3')
# parse the arguments
args = parser.parse_args()

# At this point, the arguments will be:
# Argument          Values      Description
# args.posArg1      string
# args.posArg2      string
# args.optArg1      string
# args.optArg2      string
# args.optTFArg1    True/False
# args.me1          True/False
# args.me2          True/False
# args.me3          True/False

# Put the begin mark here, after the arg parsing, so argument problems are
# reported first.
print('**** Begin Processing ****')
# get start processing time
procStart = datetime.now()
print('    Process start time: ' + procStart.strftime('%m/%d/%Y %H:%M:%S'))

# Process the arguments
if args.posArg1 is not None:
    print(args.posArg1)
else:
    # arg is none, so print a message.
    # Not actually possible, since this is a positional argument.
    # Inclued here so we can see how to process arguments.
    print('No value for posArg1.')


#get end  processing time
procEnd = datetime.now()
print('\n**** End Processing ****')
print('    Process end time: ' + procEnd.strftime('%m/%d/%Y %H:%M:%S'))
print('    Duration: ' + str(procEnd - procStart) + '\n')