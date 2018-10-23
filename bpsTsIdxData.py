#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# imports
#
# system related
import sys
# date and time stuff
from datetime import datetime, time
from pandas.tseries.frequencies import to_offset
from dateutil import parser as duparser

# numerical manipulation libraries
import numpy as np
import pandas as pd

# Class: TsIdxData
# File: TsIdxData.py
#
# Timestamped Indexed Data
#
# This file implements an data contaner which holds time stamped values,
# indexed and sorted by time stamp. The data container is implemented as a
# Pandas Dataframe.  The timestamp is a Datetime, and the values are floats. 
#
# The source data used to populate the container can have multiple value
# columns, but one column needs have a name which matches yName. This column
# will be considered the "value" column.  
#
# The source data used to populate the container also must have one value
# column or an index column with a name that matches tsName. This column will be
# used as the index.
#
# The constructor is expecting a data frame which is used as the source data.
#
# The constructor (ctor) has these areguments:
#   name -- The name to give the object. An instrument name for example.
#
#   tsName -- The name of the timestamp (index) column.
#
#   yName -- The name of the value column.
#
#   df -- The source data used to populate the data container. If a data frame
#         is not specified, then an empty data frame is created.  See
#         "Data Structure Notes" below.
#
#   valueQuery -- Query string used to filter the dataset.
#                 Default is empty, so nothing is filtered out. Use "val" to
#                 represent the process value(s). Use "==" for an equality test.
#                 For example, to filter out all values < 0 or > 100, you want 
#                 to keep everything else,so the filter string would be:
#                   "val >= 0 and val <= 100".
#
#   startQuery -- Datetime string used to filter the dataset.  Data timestamped
#                 before this time will be filtered out. The default is empty,
#                 so no data is filtered out if nothing is specified.
#
#   endQuery -- Datetime string used to filter the dataset.  Data timestamped
#               after this time will be filtered out. The default is empty,
#               so no data is filtered out if nothing is specified.
#
#   sourceTimeFormat -- Specify the time format of the source data timestamp.
#                       If nothing is specified, the value defaults to
#                       "%m/%d/%Y %H:%M:%S.%f". A string using the following
#                       symbolic placeholders is used to specify the format: 
#                           %m minutes, %d days, %Y 4 digit year, 
#                           %y two digit year, %H hours (24hr format),
#                           %I hours (12 hr format), %M minutes, %S seconds,
#                           %f for fractional seconds (e.g. %S.%f), %p AM/PM.
#
# DATA STRUCTURE NOTES
#   The source data must have the following structure:
#       Timestamp data: An index or value column must exist
#                       labeled with the tsName specified.  This data must be of 
#                       type datetime or convertable to datetime. It will
#                       be converted, if needed, to a datetime the format
#                       specified with the sourceTimeFormat string.
#
#       Value data:     A value (non-index) column must exist labeled with the 
#                       yName specified. This data msut be of type float or
#                       or convertable to a float. It will be converted if needed.
#
#                       Other value (non-index) columns are allowed, the names 
#                       don't matter, as long as one of them is named yName
#                       per above.
#      
#
# In addition the data can be resampled, using the resample(args, stats) method.
# Resampling makes the most sense when the original data has time stamps at 
# regular intervals, and the interval needs# to be changed.
# If the data is being upsampled (increase the frequency),
# than values will be forward filled to populate gaps in the data. If the data
# is being downsampled (decrease in frequency), then the specified stats will
# be calculated on values that fall between those being sampled.
#
# When resampling, and data is being downsampled, stats can be calculated. The
# stats parameter is used to specify which stats to calculate.  It is optional
# and defaults to 'm' if not specified. Choices are: (V)alue, m(I)n, ma(X),
# (a)verage/(m)ean, and (s)tandard deviation.
# The (a) and (m) options do the same thing. Choices are not case sensitive.
# Default is average/mean (m).  In the case of the Value option,
# the first value available which is on or after the timestamp is shown.
# The values between this and the next sample point are thrown away.
# For the other options, the intermediate values are used to calculate the
# statistic.  Note: The stats parameter is ignored when upsampling.
#
# The member data can be appended to using the appendData(dataframe) method.
#
# The member data can be replaced using the replaceData(dataframe) method.
#
# The following read only properties are implemented
#    name
#       string -- object name
#
#    tsName
#       timestamp -- column name
#
#    valueQuery
#       string used to query the source data during construction
#
#   indexName 
#       string name of the index
#
#   index
#       an array of data about the index, including the index data, datatype, and name
#
#    columns
#       dictionary with column names as the key and the data type as a value {col name : datatype, ...}
#
#    data
#        a copy of the dataframe
#
#    timeOffset
#        time period between data samples
#
#     startTs
#         start time filter used to query the source data during construction
#    
#     endTs
#        end time filter used to query the source data during construction 
#
#     count
#        the number of rows in the data frame 
#
#     isEmpty
#       boolean true if data frame is empty
#
#
class TsIdxData(object):
    def __init__(self, name, tsName=None, yName=None, df=None,
            valueQuery=None, startQuery=None, endQuery=None,
            sourceTimeFormat='%m/%d/%Y %H:%M:%S.%f', 
            forceColNames=False):
        self._name = str(name) # use the string version

        # default x-axis (timestamp) label to 'timestamp' if nothing is specified
        if tsName is None:
            self._tsName = 'timestamp'
        else:
           self._tsName = str(tsName) # use the string version

        # default the y-axis label to the name if nothing is specified
        if yName is None:
            self._yName = name
        else:
           self._yName = str(yName) # use the string version

        # Keep the column (header) names as a property
        self._columns = [self._tsName, self._yName]

        # Default the value query to empty if not specified. 
        if valueQuery is None:
            self._vq = ''
        else:
            # something specified for the value  query string (vq)
            # make sure it is a string, and convert to lower case
            self._vq = str(valueQuery).lower()

        # Convert the start and end times to datetimes if they are specified.
        # Use the dateutil.parser function to get input flexability, and then
        # convert to a pandas datetime for max compatibility
        # If time info is not included in the start time, it defaults to
        # midnight, so comparisons will work as expected and capture the entire
        # day. For the end time, however, if time info is not included, force
        # it to be 11:59:59.999 so the entire end date is captured.
        if startQuery is None:
            self._startQuery = None
        else:
            # see if it is already a datetime. If it is, no need to do
            # anything. If it isn't then convert it. If there is a conversion
            # error, set to none and print a message
            if not isinstance(startQuery, pd.datetime):
                # need to convert
                try:
                    self._startQuery = duparser.parse(startQuery, fuzzy=True)
                    # convert to a pandas datetime for max compatibility
                    self._startQuery = pd.to_datetime(self._startQuery,
                                            #format='%m/%d/%Y %I:%M:%S %p',
                                            errors='raise',
                                            box=True,
                                            infer_datetime_format=True,
                                            origin='unix')
                except (ValueError, OverflowError) as voe:
                    # not convertable ... invalid ... ignore
                    print('    WARNING: Invalid start query. Ignoring.')
                    print(voe)
                    self._startQuery = None
            else:
                # no need to convert
                self._startQuery = startQuery

        # repeat for end query
        if endQuery is None:
            self._endQuery = None
        else:
            # see if it is already a datetime. If it is, just update the member
            # anything. If it isn't then convert it. If there is a conversion
            # error, set to none and print a message
            if not isinstance(endQuery, pd.datetime):
                # need to convert
                try:
                    self._endQuery = duparser.parse(endQuery, fuzzy=True)
                    # If and end time was not specified, force it to the end
                    # of the day so the entire date is included.
                    if self._endQuery.time() == time(0,0,0,0):
                        self._endQuery = self._endQuery.replace(hour=23, minute=59, 
                                                  second=59, microsecond=999999)

                    # convert to a pandas datetime for max compatibility
                    self._endQuery = pd.to_datetime(self._endQuery,
                                                    #format='%m/%d/%Y %I:%M:%S %p',
                                                    errors='raise',
                                                    box=True,
                                                    infer_datetime_format=True,
                                                    origin='unix')
                except (ValueError, OverflowError) as voe:
                    # not convertable ... invalid ... ignore
                    print('    WARNING: Invalid end query. Ignoring.')
                    print(voe)
                    self._endQuery = None
            else:
                # no need to convert. Update the member
                self._endQuery = endQuery

                # If and end time was not specified, force it to the end
                # of the day so the entire date is included.
                if self._endQuery.time() == time(0,0,0,0):
                    self._endQuery = self._endQuery.replace(hour=23, minute=59, 
                                              second=59, microsecond=999999)

                # convert to a pandas datetime for max compatibility
                self._endQuery = pd.to_datetime(self._endQuery, errors='coerce',
                                        box=True,
                                        infer_datetime_format=True,
                                        origin='unix')

        # make sure the source time format is a string
        self._sourceTimeFormat = str(sourceTimeFormat)

        # Now deal with the data
        # Get the specified data into the member data. 
        # Trying to make a new dataframe allows something like a dataframe
        # to be used (like a list, dict, or other dataframe.
        # If it isn't possible to build a dataframe from what, then assign an 
        # empty dataframe.
        try:
            self._df = pd.DataFrame(df)
        except ValueError as ve:
            print('    WARNING: The data specified when building ' + self.name \
+ ' cannot be used to make a dataframe.  An empty dataframe is being used.')
            print(ve)
            self._df = None # so that an empty dataframe will be used below

        if df is None or self._df is None:
            # No (valid) source specified ...
            # create an empty data frame
            # not resampling ...
            # create an empty data frame with the column names
            self._df = pd.DataFrame(columns=[self._tsName, self._yName])
            # force the columns to have the data types of datetime and float
            self._df[self._yName] = self._df[self._yName].astype('float',
                                                    errors='ignore')

            # force the timestamp to a datetime
            # should not raise an error, as there is no data 
            self._df[self._tsName] = pd.to_datetime(self._df[self._tsName],
                                                    errors='coerce')
            # set the timestamp as the index
            self._df.set_index(self._tsName, inplace=True)

            # set the other properties
            self._timeOffset = np.NaN
        else:
            # Source data is specified ...
            # Use the member function to process it into the form we need.
            self._df = pd.DataFrame(columns=[self._tsName, self._yName])
            self._df = self.__massageData(srcDf=df, forceColNames=forceColNames)
            # Use the member function to apply the filters
            self._df = self.__filterData()

            # Get the inferred frequency of the index. Store this internally,
            # and expose below as a property.  Sometimes the data has repeated
            # timestamps, and infer_freq does not work.Try it, but if it comes up
            # empty, try it manually
            try:
                # try the inferred frequency
                inferFreq = pd.infer_freq(self._df.index)
            except TypeError as te:
                print('    WARNING: Timestamp column does not appear to be a datetime. \n \
Cannot infer a frequency. Will try to do so manually by comparing the first few values.')
                print(te)
                inferFreq = None
            except ValueError as ve: 
                print('    WARNING: There are not enough timestamps to infer a frequency. \n \
Will try to do so manually by comparing the first few values.')
                print(ve)
                inferFreq = None
            finally:
                # Try to get an inferred freq if the above did not work
                # If that did not work, try to get it manually. When timestamps are
                # repeated, it looks like the odd/even rows in that order are
                # repeated.
                if inferFreq is None or inferFreq == pd.Timedelta(0): 
                    print('    WARNING: Data may have very few, skipped, missing, repeated or corrupted timestamps.\n \
Determining sampling frequency manually.')
                    # Use 3 and 4 if possible, just in case there is
                    # something strange in the beginning. Otherwise, use entries 0
                    # and 1, or give up, and use 1 second.
                    if len(self._df.index) >= 4:
                        inferFreq = pd.Timedelta((self._df.index[3] -
                                                  self._df.index[2]))
                    elif len(self._df.index) >= 2:
                        inferFreq = pd.Timedelta((self._df.index[1] - self._df.index[0]))
                    else:
                        print('    WARNING: Not enough data to determine the \
data frequency. Using 1 sec.')
                        inferFreq = pd.Timedelta('1S')

                # At this point, there is value for inferred frequency,
                # but there may be repeated times due to sub-second times being
                # truncated.  If this happens, the time delta will be 0. Deal
                # with it by forcing 1 second
                if inferFreq == pd.Timedelta(0):
                    print('    WARNING: Two rows have the same timestamp. \
Assuming a 1 second data frequency.')
                    inferFreq = pd.Timedelta('1S')

                # Frequency is ready. Convert it and store it as a time offset.
                self._timeOffset = to_offset(inferFreq)

            # ctor all done!

    def __repr__(self):
        outputMsg=  '{:13} {}'.format('\nName: ', self._name + '\n')
        if self.isEmpty: 
            outputMsg+= 'Contains no data!\n'
            outputMsg+= '{:13} {}'.format('Length: ', str(self.count) + '\n')
            return (outputMsg)
        else:
            outputMsg+= '{:13} {:18} {:10} {}'.format('Index: ', self._df.index.name, \
'datatype: ', str(self._df.index.dtype) + '\n')
            outputMsg+= 'Columns:\n'
            for col in self.columns:
                outputMsg+= '{:4} {:15} {} {}'.format(' ', col, self.columns[col], '\n')
            outputMsg+= '{:13} {}'.format('Value Query: ', self._vq + '\n')
            outputMsg+= '{:13} {}'.format('Start Time: ', str(self.startTs) + '\n')
            outputMsg+= '{:13} {}'.format('End Time: ', str(self.endTs) + '\n')
            outputMsg+= '{:13} {}'.format('Period: ', str(self._timeOffset) + '\n')
            outputMsg+= '{:13} {}'.format('Length: ', str(self.count) + '\n\n')
            outputMsg+= 'Data:' + self._df.to_string()
            return(outputMsg)

    def resample(self, resampleArg='S', stats='m'):
        # Resample the data from the complete dataframe.
        # The original data is replaced with the resampled data.
        # Determine if we are up or down sampling by comparing the
        # specified frequency (time offset) with the data frequency.
        # If the data is being upsampled (increase the frequency), than values
        # will be forward filled to populate gaps in the data.
        # If the data is being downsampled (decrease in frequency), then the
        # specified stats will be calculated on values that fall between those
        # being sampled.
        #
        # stats (optional, default='m') Choose which statistics to calculate when
        # resampling. Choices are: (V)alue, m(I)n, ma(X), (a)verage/(m)ean,
        # and (s)tandard deviation. The (a) and (m) options do the same thing.
        # Choices are not case sensitive. Default is 
        # average/mean.  In the case of the Value option, the first value available
        # which is on or after the timestamp is shown. The values between this and the
        # next sample point are thrown away. For the other options, the intermediate
        # values are used to calculate the statistic.
        #
        # Make sure the resample argument is valid
        if resampleArg is None:
            # no sample period specified, use 1 second
            print('    WARNING: ' + self._name + ': No resample period \
specified. Using 1 Second.')
            resampleTo = to_offset('S')
        else:
            try:
                resampleTo = to_offset(resampleArg)
            except ValueError as ve:
                print('    WARNING: ' + self._name + ': Invalid resample \
period specified. Using 1 second.')
                print(ve)
                resampleTo = to_offset('S')

        if resampleTo < self._timeOffset:
            # Data will be upsampled. We'll have more rows than data.
            # Forward fill the data for the new rows -- a new row will use the
            # previous recorded value until a new recorded value is available.
            # In other words -- carry a value forward until a new one is avail.
            # The stats argument is ignored.
            
            # If stats were specified, print a message about not using the specified stats
            if stats is not None or not stats:
                print('    WARNING: Data is being upsampled. There will be more \
rows than data. \nCalculating statistics on repeated values does not make sense, \
and a non-empty stat parameter was specified.\n The "stats" parameter will be ignored. \n \
Set "stats" to an empty string ("") or "None" to eliminate this warning.\n')

            # Create a new data frame with a timestamp and value column, and 
            # force the data type to timestamp and float
            dfResample = pd.DataFrame(columns=[self._tsName])
            dfResample[self._yName] = np.NaN
            dfResample = dfResample.astype({self._yName: float}, errors = 'ignore')
            dfResample[self._tsName] = \
                pd.to_datetime(dfResample[self._tsName], errors='coerce')

            # set the timestamp as the index
            dfResample.set_index(self._tsName, inplace=True)
            # upsample the data
            try:
                dfResample[self._yName] = \
                        self._df.iloc[:,0].resample(resampleTo).pad()
                # print a message
                print('    ' + self.name + ': Upsampled from ' \
                    + str(self._timeOffset) + ' to ' + str(resampleTo))
                # update the object frequency
                self._timeOffset = resampleTo
                # now overwrite the original dataframe with the resampled one
                # and delete the resampled one
                self._df = dfResample
                del dfResample
                return
            except ValueError as ve:
                print('    WARNING: ' + self._name + ': Unable to resample \
data. Data unchanged. Frequency is ' + str(self._timeOffset))
                print(ve)
                return
        elif resampleTo > self._timeOffset:
            # Data will be downsampled. We'll have more data than rows.
            # This means we can calculate statistics on the values between
            # those being displayed.  Use the stats option to determine which
            # stats are to be calculated.

            # make stats not case sensitive
            if stats is not None:
                self._stats = str(stats).lower()
            else:
                self._stats = ''

            # Determine column names.
            # Determine the stat flags. These are used below to decide which
            # columns to make and calculate. Display the stat if the representative
            # character is in the stats argument. Find returns -1 if not found
            displayValStat = self._stats.find('v') > -1   # value
            displayMinStat = self._stats.find('i') > -1   # minimum
            displayMaxStat = self._stats.find('x') > -1   # maximum
            # mean or average
            displayMeanStat = self._stats.find('m') > -1 or self._stats.find('a') > -1
            # standard deviation
            displayStdStat = self._stats.find('s') > -1 or self._stats.find('d') > -1
            # If none of the flags are set, an invalid string must have been
            # passed. Display just the mean, and set the stats string accordingly
            if not displayValStat and not displayMinStat and \
               not displayMaxStat and not displayMeanStat and \
               not displayStdStat:
                displayMeanStat = True
                self._stats = 'm'
                
            minColName = 'min_' + self._name
            maxColName = 'max_' + self._name
            meanColName = 'mean_'+ self._name
            stdColName = 'std_' + self._name

            # Create a new data frame with a timestamp and value column(s), and 
            # force the data type(s) to timestamp and float
            dfResample = pd.DataFrame(columns=[self._tsName])
            if displayValStat:
                dfResample[self._yName] = np.NaN
                dfResample = dfResample.astype({self._yName: float}, errors = 'ignore')
            if displayMinStat:
                dfResample[minColName] = np.NaN
                dfResample = dfResample.astype({minColName: float}, errors = 'ignore')
            if displayMaxStat:
                dfResample[maxColName] = np.NaN
                dfResample = dfResample.astype({maxColName: float}, errors = 'ignore')
            if displayMeanStat:
                dfResample[meanColName] = np.NaN
                dfResample = dfResample.astype({meanColName: float}, errors = 'ignore')
            if displayStdStat:
                dfResample[stdColName] = np.NaN
                dfResample = dfResample.astype({stdColName: float}, errors = 'ignore')

            # force the timestamp to a datetime datatype
            dfResample[self._tsName] = \
                pd.to_datetime(dfResample[self._tsName], errors='coerce')

            # set the timestamp as the index
            dfResample.set_index(self._tsName, inplace=True)

            # now do the resampling for each column
            # NOTE: fractional seconds can make merging appear to behave
            # strangely if precision gets truncated.
            try:
                if displayValStat:
                    dfResample[self._yName] = \
                            self._df.iloc[:,0].resample(resampleTo,
                            label='right', closed='right').last()

                if displayMinStat:
                    dfResample[minColName] = \
                            self._df.iloc[:,0].resample(resampleTo,
                            label='right', closed='right').min()

                if displayMaxStat:
                    dfResample[maxColName] = \
                            self._df.iloc[:,0].resample(resampleTo,
                            label='right', closed='right').max()

                if displayMeanStat:
                    dfResample[meanColName] = \
                            self._df.iloc[:,0].resample(resampleTo,
                            label='right', closed='right').mean()

                if displayStdStat:
                    dfResample[stdColName] = \
                            self._df.iloc[:,0].resample(resampleTo,
                            label='right', closed='right').std()
                # print a message
                print('    ' + self._name + ': Downsampled from ' + \
                      str(self._timeOffset) + ' to ' + str(resampleTo))
                # update the object frequency
                self._timeOffset = resampleTo
                # now overwrite the original dataframe with the resampled one
                # and delete the resampled one
                self._df = dfResample
                del dfResample
                return
            except ValueError as ve:
                print('    WARNING: ' + self._name + ': Unable to resample \
data. Data unchanged. Frequency is ' + str(self._timeOffset))
                print(ve)
                return
        else:
            # resampling not needed. Specified freq matches data already
            print('    ' + self._name + ': Resampling not needed. New frequency \
matches data frequency. Data unchanged. Frequency is ' + str(self._timeOffset))
            return
           
    def appendData(self, srcDf, IgnoreFirstRows=1):
        # This function takes a source data frame (srcDf) and appends it to the 
        # member data frame, as long as srcDf is a dataframe.
        # The column names of the source data are ignored, but 
        # it is expected that index is or can be converted to a datetime, and the
        # values are or can be converted to a float.  Use IgnoreFirstRows to set
        # how many rows to throw away before merging the data. Default is 1, so as
        # to ignore a header row. Setting IgnoreFirstRows to 0 will treat every
        # row as data.
        
        # Get the source data into a temp dataframe. Use member column names.
        # This allows something like a dataframe to be used (like a list, dict,
        # or other dataframe. If it isn't possible to build a dataframe from what
        # was passed in, print a message and punt.
        #
        # If duplicate timestamps exist after the merge, duplicates will be dropped
        # keeping the last value found in the list.
        try:
            df_temp = pd.DataFrame(data=srcDf, columns=[self._yName])
        except ValueError:
            print('    WARNING: The data specified for the appendData function \
could not be turned into a dataframe. Nothing appended.')
            return

        # drop rows that should be ignored
        if 1 <= IgnoreFirstRows:
            df_temp.drop(df_temp.index[:IgnoreFirstRows], inplace=True)

        # condition and filter the passed in dataframe
        df_temp = self.__massageData(df_temp)
        df_temp = self.__filterData(df_temp)

        # now merge the conditioned data with the member data, along the index
        # (timestamp) axis
        self._df = self._df.append(df_temp)

        # The merge may have made duplicate indexes. Drop them, but this requires
        # resetting and rebuilding the index.
        self._df.reset_index(drop=False, inplace=True)
        self._df.drop_duplicates(subset=self._tsName, keep='last', inplace=True)
        self._df.set_index(self._tsName, inplace=True)
        self._df.sort_index(inplace=True)
        return

    # drop existing data and replace it with the specified dataframe, as long
    # as the passed in thing is a dataframe, otherwise do nothing.
    def replaceData(self, srcDf, IgnoreFirstRows = 1):
        # This function takes a source data frame (srcDf) and replaces the 
        # member dataframe with it, as long as srcDf is a dataframe.
        # The column names of the source data are ignored, but 
        # it is expected that index is or can be converted to a datetime, and the
        # values are or can be converted to a float.  Use IgnoreFirstRows to set
        # how many rows to throw away before merging the data. Default is 1, so as
        # to ignore a header row. Setting IgnoreFirstRows to 0 will treat every
        # row as data.
        
        # Get the source data into a temp dataframe. Use member column names.
        # This allows something like a dataframe to be used (like a list, dict,
        # or other dataframe. If it isn't possible to build a dataframe from what
        # was passed in, print a message and punt.
        try:
            df_temp = pd.DataFrame(data=srcDf, columns=[self._yName])
        except ValueError:
            print('    WARNING: The data specified for the replaceData function \
could not be turned into a dataframe. The data was not replaced.')
            return

        # drop rows that should be ignored
        if 1 <= IgnoreFirstRows:
            df_temp.drop(df_temp.index[:IgnoreFirstRows], inplace=True)

        # condition and filter the passed in dataframe.
        # The member data will be updated.
        self._df = self.__massageData(df_temp)
        self._df = self.__filterData()
        return

    # Private member function to massage a specified dataframe, and return 
    # the resulting dataframe. 
    # If no source data is specified, the memeber data is used as the soruce.
    #
    # This function assumes the source is a dataframe with at least an index and
    # a column, or two columns, or an object that could be converted to such a
    # thing. It will try and turn one column into a timestamp index,
    # and another it will try turn into a float value column.
    # Before finishing:
    #   The timestamp will be changed to a datetime (if needed)
    #   The value will be turned into a float (if needed)
    #   The timestamp will be rounded to milliseconds
    #   The dataframe will be sorted by timestamp
    #   Duplicate timestamps will be removed, and the last value will be the one used.
    # Additional columns are ignored/unchanged, other than rows will removed 
    # from the additional column where the corresponding value or timestamp is
    # NaN/NaT, or the timestamp is a duplicate.
    #
    # The timestamp column must be a datetime or convertible to a datetime
    # and either needs to be the index or a value column.
    # The value column needs to be a float or convertible to a 
    # float.
    #
    # If forceColNames is true, check for correctly named columns and use them
    # if they are present. Otherwise assume the index is the timestamp if it is
    # a datetime, or use the 1st col as the timestamp if the index is not a
    # datetime. Use the 2nd column as the value if the index is not a datetime,
    # or use the 1st column as the value if the index is a datetime.
    #
    # If forceColNames is false (default), the timestamp name must match the
    # string in self._tsName, and the value name must match the string in 
    # self._yName. 
    #
    # Returns a DataFrame
    #
    # Exceptions raised:
    #   NameError if value or timestamp column name cannot be found in the df.
    #   TypeError if a dataframe or something like it is passed in for 
    #       the source dataframe.

    def __massageData(self, srcDf=None, forceColNames=False):
        # self is not defined when the default params are evaluated, so can't
        # use srcDf=self._df 
        # do this as a work around
        if srcDf is None:
            srcDf=self._df
        
        # make sure a dataframe, or something that can be converted to
        # dataframe is passed in, otherwise leave.
        try: 
            df_srcTemp = pd.DataFrame(srcDf)
        except TypeError as te:
            print('    ERROR Processing ' + self._name + '.\n \
The private member function __massageData was not passed source data that can \
be converted to a dataframe. No data was changed.')
            print(te)
            raise te

        # Get the column and index names.
        dfCols = df_srcTemp.columns
        dfIndex = df_srcTemp.index.name

        # Set the column names if they are being forced.
        # Assume the index is the timestamp if it is a datetime, or the 
        # 1st col is the timestamp if the index is not a datetime.
        # Use the 2nd column as the value if the index is not a datetime,
        # or use the 1st column as the value if the index is a datetime.
        
        if forceColNames:
            # see if the names exist and use them if they do
            # timestamp name
            if self._tsName == dfIndex or self._tsName in dfCols:
                # Timestamp name is the index or a column name. Nothing to do.
                # Here for completeness and possible future use. Reorder the 
                # non-index case to leftmost column.
                pass
            else:
                # timestamp name isn't the index or a column name.
                # If the index is a datetime datatype, assume this should
                # be the timestamp column and name it. Otherwise, assume the
                # leftmost column is the timestamp.
                if 'datetime64[ns]'==df_srcTemp.index.dtype:
                    df_srcTemp.index.rename(self._tsName, inplace=True)
                else:
                    df_srcTemp.rename(columns={dfCols[0]: self._tsName}, inplace=True)

            # value column name
            if self._yName in dfCols:
                # value name is already a column name. Nothing to do.
                # Here for completeness and possible future use. Reorder
                # to the second column from the left?
                pass
            else:
                # Value name isn't already a column name.
                # If the index is a datetime, assume the value is the 1st column,
                # otherwise, assume the value is the second column.
                if 'datetime64[ns]'==df_srcTemp.index.dtype:
                    df_srcTemp.rename(columns={dfCols[0]: self._yName}, inplace=True)
                else:
                    df_srcTemp.rename(columns={dfCols[1]: self._yName}, inplace=True)
            
            # update the column and index names
            dfCols = df_srcTemp.columns
            dfIndex = df_srcTemp.index.name
                
        # If the column names were force, they should be correct and pass
        # the tests below. If not, a name error may be raised.
        # Verify the correct column and/or index names exist. If not raise a NameError 
        if not (self._yName in dfCols) or \
                not (self._tsName in dfCols or self._tsName == dfIndex):
                    # source data column names are not as needed. Raise a name error:
            try:
                if not (self._yName in dfCols):
                # value column name not found in the df_srcTemp. Raise a NameError
                    raise NameError('    ERROR Processing ' + self._name + '.\n \
The data cannot be processed because a column named "' + self._yName + '" is \
needed. It is used as the value column.')
            except NameError as ne:
                    print(ne)
                    print('The column names found in the data are:')
                    print(dfCols)
                    raise ne
            
            try:
                if not (self._tsName in dfCols or self._tsName == dfIndex):
                    # There is no index or value column name the same as the timestamp
                    # name. Raise a NameError.
                    raise NameError('    ERROR Processing ' + self._name + '.\n \
The data cannot be processed because the index or a value column needs to be \
named "' + self._tsName + '". It is used as the timestamp.')
            except NameError as ne:
                print(ne)
                print('The column names found in the data are:')
                print(dfCols)
                print('The index is named: "' + dfIndex + '".')
                raise ne

        # At this point the column names are as needed. The timestamp may be a 
        # value column or the index.
        #
        # Change the value column to a float if needed. Issue a warning, but 
        # do the best conversion possible in any event.
        if 'float64' != df_srcTemp[self._yName].dtype:
            try:
                df_srcTemp[self._yName] = df_srcTemp[self._yName].astype('float',
                                                                errors='raise')
            except ValueError as ve:
                print('    WARNING: There was a problem converting at least one \
value into a float. The conversion did the best conversion possible.')
                print(ve)
                df_srcTemp[self._yName] = df_srcTemp[self._yName].astype('float',
                                                                errors='ignore')

        # As an intermediate step, we want the df_srcTemp to have the timestamp as a 
        # datetime value column (not the index) so we can more easily drop dups,
        # round time, etc.  The following matrix is used to decide what to do
        # ----------------------------------------------------------------------------
        # idx name      |col name   |           |
        # matches       |matches    |datetype is|
        # self._tsName  |self._yName|datetime   |action
        # ----------------------------------------------------------------------------
        # No            | No        | don't care| Delt with above. Not poss. here
        # ----------------------------------------------------------------------------
        # Yes           | No        | No        | Reset index to a val col
        #               |           |           | Change datatype to datetime
        # ----------------------------------------------------------------------------
        # Yes           | No        | Yes       | Reset index to val col
        # ----------------------------------------------------------------------------
        # Yes           | Yes       | No        | Drop col
        #               |           |           | Reset index to a val col
        #               |           |           | Change datatype to datetime
        # ----------------------------------------------------------------------------
        # Yes           | Yes       | Yes       | Drop col
        #               |           |           | Reset index to a val col
        # ----------------------------------------------------------------------------
        # No            | Yes       | No        | Change datatype to datetime
        # ----------------------------------------------------------------------------
        # No            | Yes       | Yes       | No action needed here
        # ----------------------------------------------------------------------------
      
        # See if there is an index and column that match the timestamp name.
        # If there is, print a message, and drop the column.
        if self._tsName == dfIndex and (self._tsName in dfCols):
            print('Processing ' + self._name + '.  The index and a value column \
both match the timestamp name "' + self._tsName + '". Dropping the column, \
and keeping the index.' )
            df_srcTemp.drop(columns=[self._tsName], inplace=True, errors='ignore')

        # Now see if the index name matches the timestamp name. If it does,
        # reset the index so the indexed timestamp becomes a normal value column.
        if self._tsName == dfIndex:
            df_srcTemp.reset_index(drop=False, inplace=True)

        # Now there is a timestamp value column. See if it is the correct datatype.
        # Convert it if needed.
        if 'datetime64[ns]' != df_srcTemp[self._tsName].dtype:
            try:
                # For changing to timestamps, coerce option for errors mayh  mark
                # some dates as NaT.
                # Try it with raise first and then resort to coerce if needed.
                df_srcTemp[self._tsName] = pd.to_datetime(df_srcTemp[self._tsName],
                                                        errors='raise',
                                                        box = True, 
                                                        format=self._sourceTimeFormat,
                                                        exact=False,
                                                        #infer_datetime_format = True,
                                                        origin = 'unix')
            except ValueError as ve:
                print('    WARNING: Processing ' + self._name + '. There was \
a problem converting some timestamps. Timestamps may be incorrect, and/or some \
rows may be missing.')
                print(ve)
                df_srcTemp[self._tsName] = pd.to_datetime(df_srcTemp[self._tsName],
                                                    errors='coerce',
                                                    box = True, 
                                                    infer_datetime_format = True,
                                                    origin = 'unix')

        # Now the column names and data types are correct.    
        # Condition the data and (re)index it.
        # Get rid of any NaN/NaT values in either column. These can be from the
        # original data or from invalid conversions to float or datetime.
        df_srcTemp.dropna(subset=[self._tsName, self._yName], how='any', inplace=True)
        # Rround the timestamp to the nearest ms. Unseen ns and
        # fractional ms values are not always displayed, and can cause
        # unexpected merge and up/downsample results.
        try:
            df_srcTemp[self._tsName] = df_srcTemp[self._tsName].dt.round('L')
        except ValueError as ve:
            print('    WARNING: Timestamp cannot be rounded.')
            print(ve)

        # Get rid of any duplicate timestamps. Done after rounding in case rouding
        # introduced dups.
        df_srcTemp.drop_duplicates(subset=self._tsName, keep='last', inplace=True)

        # Now the data type is correct, and foreseen data errors are removed.
        # Set the index to the timestamp column and sort it.
        # Set the member dataframe to the massaged data
        df_srcTemp.set_index(self._tsName, inplace=True)

        # All done. Data in indexed by timestamp, and there is a correctly 
        # named value column.  There are no NaN/NaT values, timestamps have been 
        # rounded to mSec, and there are no duplicate timestamps.
        return df_srcTemp.sort_index(inplace=False)

        # end of def __massageData(self, srcDf):

    # Private member function to apply the value query and the timestamp filter
    # to a specified dataframe, and return the resulting dataframe.
    # If no source dataframe is specified, the member dataframe is used.
    def __filterData(self, srcDf=None):
        # self is not defined when the default params are evaluated, so can't
        # use srcDf=self._df
        # do this as a work around
        if srcDf is None:
            srcDf=self._df
        
        # make sure a dataframe, or something that can be converted to a
        # dataframe is passed in, otherwise leave.
        try: 
            df_temp = pd.DataFrame(srcDf)
        except TypeError as te:
            print('    ERROR Processing ' + self._name + '.\n \
The private member function __filterData was not passed anything that can \
be converted to a dataframe. No data was changed.')
            print(te)
            raise te
                
        # Apply the query string if one is specified.
        # Replace "val" with the column name.
        if self._vq != '':
            queryStr = self._vq.replace("val", self._yName)
            # try to run the query string, but ignore it on error
            try:
                df_temp.query(queryStr, inplace = True)

            except ValueError:
                print('    WARNING: Invalid query string. Ignoring the \
specified query when appending data.')

        # Timestamp is the index, so filter based on the specified
        # start and end times.
        # Non specified times will be None, so the filter still works as
        # is. If both are none, no filtering is performed.
        # Either way, set the member dataframe to the result
        return df_temp.loc[self._startQuery : self._endQuery]
        # end of def __filterData(self, srcDf=None):

    # read only properties
    @property
    def name(self):
        return self._name

    @property
    def tsName(self):
        return self._tsName
           
    @property
    def valueQuery(self):
        return self._vq

    @property
    def indexName(self):
        return self._df.index.name
    
    @property
    def index(self):
        return self._df.index

    @property
    def columns(self):
        # this dictionary will include column names as the key and the data
        # type as a value
        # {col name : datatype, ...}
        return dict(self._df.dtypes)

    @property
    def data(self):
        return self._df

    @property
    def timeOffset(self):
        return self._timeOffset

    @property
    def startTs(self):
        # assumes index is sorted and start is at the top
        return self._df.index[0]

    @property
    def endTs(self):
        # assumes index is sorted and end is at the bottom
        return self._df.index[-1]

    @property
    def count(self):
        return len(self._df.index)

    @property
    def isEmpty(self):
        return self._df.empty 

