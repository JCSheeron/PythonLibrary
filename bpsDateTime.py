#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bpsDateTime.py
#
# System and typing related
from typing import Optional

# Date and Time related functions
from datetime import datetime, time as dttime
from dateutil import parser as duparser


# def adjMissingTime(dt: datetime, ts: Optional[dttime] = dttime.max) -> datetime:
def adjMissingTime(dt: datetime, ts: dttime = dttime.max) -> datetime:
    """Adjust the time if missing.

    Return a datetime with date information that matches the specified
    datetime (dt), but with time informaiton that matches the specified time (ts).
    The time defaults to one moment before midnight, such that if the functions
    is called without ts being specified, dt will be adjusted to be midnight.

    This is useful for "end dates" such that the associated time will span the
    entire day.
    """
    # check for time info to be all zeros (midnight) and force to the specified time in this case.
    if dt.time() == dttime():
        if ts is not None and isinstance(ts, dttime):
            dt = dt.replace(
                hour=ts.hour,
                minute=ts.minute,
                second=ts.second,
                microsecond=ts.microsecond,
            )
    return dt


def getAuxDates(
    startDt=None, endDt=None, auxStartDt=None, auxEndDt=None
) -> tuple[Optional[datetime], Optional[datetime]]:
    """Return a (datetime, datetime) tuple that has aux start/end times.

    The returned tuple will have start/end times that are not outside the
    range defined by startDt and endDt. All Dt arguments are expected to
    be convertible to a datetime. A "fuzzy" conversion is used so the
    format is reasonably flexible (4/20/1990, 20-Apr-90, etc work).
    None is assumed for a value if an argument cannot be converted to a datetime.
    Return None if there is no information (no argument provided, or
    argument is not convertible to a datetime).

    Return tuple values are per the table below:

    | ST   | ET   | AuxST | AuxET |  Return          | Notes
    -----------------------------------------------------------------------------
    | none | none | none  | none  | (none, none)     |
    | none | none | auxSt | none  | (auxSt, none)    |
    | none | none | none  | auxEt | (none, auxEt)    |
    | none | none | auxSt | auxEt | (auxSt, auxEt)   |
    | st   | none | none  | none  | (st, none)       |
    | st   | none | auxSt | none  | (auxSt', none)   | auxSt' >= st
    | st   | none | none  | auxEt | (st, auxEt)      |
    | st   | none | auxSt | auxEt | (auxSt', auxEt)  | auxSt' >= st
    | none | et   | none  | none  | (none, et)       |
    | none | et   | auxSt | none  | (auxSt, et)      |
    | none | et   | none  | auxEt | (none, auxEt')   | auxEt' <= et
    | none | et   | auxSt | auxEt | (auxSt, auxEt')  | auxEt' <= et
    | st   | et   | none  | none  | (st, et)         |
    | st   | et   | auxSt | none  | (auxSt', et)     | auxSt' >= st
    | st   | et   | none  | auxEt | (st, auxEt')     | auxEt' <= et
    | st   | et   | auxSt | auxEt | (auxSt', auxEt') | auxSt' >= st, auxEt' <= et

    Where "'" denotes a possibly modified value.

    Note that reversed start and end times are corrected by modifying the end
    time such that the end time will be >= start time, before
    the above table is applied.
    Similarly, reversed auxStartDt and auxEndDt are corrected by modifying the
    auxEndDt such that the auxEndDt >= auxStartDt before the above table is
    applied. In practice, this will mean that reversed start and end times will
    result in a 1 day range, starting and ending with the start date.
    """
    # Convet the arguments to internal datetimes, or use None. This acts to
    # validate the argumens, and convert them so datetime min/max can be used.
    # For end times, if there is no time info, force the time to midnight, so
    # if a date is specified, the entire date is included.
    if startDt is not None:
        try:
            # _st = datetime.strptime(startDt, dtFormat)
            _st = duparser.parse(startDt, fuzzy=True)
        except (ValueError, TypeError):
            _st = None
    else:
        _st = None

    if endDt is not None:
        try:
            _et = duparser.parse(endDt, fuzzy=True)
            _et = adjMissingTime(_et)
        except (ValueError, TypeError):
            _et = None
    else:
        _et = None

    if auxStartDt is not None:
        try:
            # _auxSt = datetime.strptime(auxStartDt, dtFormat)
            _auxSt = duparser.parse(auxStartDt, fuzzy=True)
        except (ValueError, TypeError):
            _auxSt = None
    else:
        _auxSt = None

    if auxEndDt is not None:
        try:
            _auxEt = duparser.parse(auxEndDt, fuzzy=True)
            _auxEt = adjMissingTime(_auxEt)
        except (ValueError, TypeError):
            _auxEt = None
    else:
        _auxEt = None

    # at this point, st, et, auxSt, and auxEt are either None or legit dates. Bust moves and
    # get on with it. Determine the tuple values per the table in the docstring.
    # Make sure the returned end time is not before the returned start time.
    #
    # This first test case is the end of the table in the docstring,
    # but is the most likely case, so test it first.
    if (
        _st is not None
        and _et is not None
        and _auxSt is not None
        and _auxEt is not None
    ):
        # make sure the end date is not before the start date (start date prioirty)
        _et = max([_st, _et])
        _auxEt = max([_auxSt, _auxEt])
        # now range check the dates
        _auxSt = max([_st, _auxSt])
        _auxEt = max([_auxSt, _auxEt])
        _auxEt = min([_auxEt, _et])
        return (_auxSt, _auxEt)
    elif _st is None and _et is None and _auxSt is None and _auxEt is None:
        return (None, None)
    elif _st is None and _et is None and _auxSt is not None and _auxEt is None:
        return (_auxSt, None)
    elif _st is None and _et is None and _auxSt is None and _auxEt is not None:
        return (None, _auxEt)
    elif _st is None and _et is None and _auxSt is not None and _auxEt is not None:
        # make sure the end date is not before the start date (start date prioirty)
        # and range check
        _auxEt = max([_auxSt, _auxEt])
        return (_auxSt, _auxEt)
    elif _st is not None and _et is None and _auxSt is None and _auxEt is None:
        return (_st, None)
    elif _st is not None and _et is None and _auxSt is not None and _auxEt is None:
        return (max([_st, _auxSt]), None)
    elif _st is not None and _et is None and _auxSt is None and _auxEt is not None:
        _auxEt = max([_st, _auxEt])
        return (_st, _auxEt)
    elif _st is not None and _et is None and _auxSt is not None and _auxEt is not None:
        # make sure the end date is not before the start date (start date prioirty)
        _auxEt = max([_auxSt, _auxEt])
        # now range check
        _auxSt = max([_st, _auxSt])
        return (_auxSt, _auxEt)
    elif _st is None and _et is not None and _auxSt is None and _auxEt is None:
        return (None, _et)
    elif _st is None and _et is not None and _auxSt is not None and _auxEt is None:
        _et = max([_auxSt, _et])
        return (_auxSt, _et)
    elif _st is None and _et is not None and _auxSt is None and _auxEt is not None:
        return (None, min([_et, _auxEt]))
    elif _st is None and _et is not None and _auxSt is not None and _auxEt is not None:
        # make sure the end date is not before the start date (start date prioirty)
        # now range check
        _auxEt = max([_auxSt, _auxEt])
        _et = max([_auxEt, _et])
        return (_auxSt, min([_et, _auxEt]))
    elif _st is not None and _et is not None and _auxSt is None and _auxEt is None:
        _et = max([_st, _et])
        return (_st, _et)
    elif _st is not None and _et is not None and _auxSt is not None and _auxEt is None:
        _auxSt = max([_st, _auxSt])
        _et = max([_auxSt, _et])
        return (_auxSt, _et)
    elif _st is not None and _et is not None and _auxSt is None and _auxEt is not None:
        _auxEt = min([_et, _auxEt])
        _auxEt = max([_st, _auxEt])
        return (_st, _auxEt)
    else:  # every case should be covered by the above. Should never get here ...
        return (None, None)
