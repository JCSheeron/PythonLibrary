This is a directory intended to contain user developed Python library
functions, classes, etc.

To ease importing into other Python modules, the PYTHONPATH can be set
to include the path to this directory. In Bash, you can add
this line the .profile file for example:
export PYTHONPATH=$PYTHONPATH:<path_of_this_directory>
It will append the specified path to the existing PYTHONPATH variable.

The functions included in this library are:

    bpsMath.py file
    Order of Magnatude (oom) functions

oomCeil(val, mag=None)
    Round value up to the next value with the same order of magnatude.
    If an order of magnatude is specified, it will be used, as long as it makes
    sense.  If it does not make sense, or if it not specified, the order
    of magnitude of the value will be used.
    Examples
    oomCeil(1805) returns 2000
    oomCeil(40050) returns 50000
    oomCeil(3521.7) returns 4000, oomCeil(3521.7, 3) returns 4000,
    oomCeil(3521.7, 2) returns 3600, oomCeil(3521.7, 1) returns 3530,
    and oomCeil(3521.7, 4) returns 10000
    Negative magnitude values are used for values between 0 and 1 or 0 and -1.
    oomCeil(0.0031) returns 0.004
    oomCeil(0.0031, -3) returns 0.004
    oomCeil(0.0031, -2) returns 0.01
    oomCeil(0.0031, -1) returns 0.1
    oomCeil(0.0031, -4) returns 0.0031

oomFloor(val, mag=None)
    Round value down to the nearest same order of magnatude value.
    If an order of magnatude is specified, it will be used, as long as it makes
    sense.  If it does not make sense, or if it not specified, the order
    of magnitude of the value will be used.
    Examples
    oomFloor(1805) returns 1000
    oomFloor(40050) returns 40000
    oomFloor(3521.7) returns 3000, oomFloor(3521.7, 3) returns 3000,
    oomFloor(3521.7, 2) returns 3500, oomFloor(3521.7, 1) returns 3520,
    oomFloor(3521.7, 4) returns 0, oomFloor(8521.7, 4) returns 0
    Negative magnitude values are used for values between 0 and 1 or 0 and -1.
    Because imprecision of floating numbers, values may vary from what is expected when
    dealing with small values, especially out to many decimal places.
    oomFloor(0.00399) returns 0.003
    oomFloor(0.00399, -3) returns 0.003
    oomFloor(0.0031, -2) returns 0.0
     oomFloor(0.0031, -1) returns 0.0
    oomFloor(0.00399, -4) returns 0.0039

oomRound(val, mag=None)
    Round value to the nearest same order of magnatude value.
    If an order of magnatude is specified, it will be used, as long as it makes
    sense.  If it does not make sense, or if it not specified, the order
    of magnitude of the value will be used.
    Examples
    oomRound(1805) returns 2000
    oomRound(40050) returns 50000
    oomRound(3521.7) returns 4000, oomRound(3521.7, 3) returns 4000,
    oomRound(3521.7, 2) returns 3600, oomRound(3521.7, 1) returns 3530,
    and oomRound(3521.7, 4) returns 10000
    Neative magnitude values are used for values between 0 and 1 or 0 and -1.
    oomRound(0.0067) returns 0.007
    oomRound(0.0067, -3) returns 0.007
    oomRound(0.0067, -2) returns 0.01
    oomRound(0.0067, -1) returns 0.0
    oomRound(0.0067, -4) returns 0.0067

Polynomial Printing
polyPrettyPrint(p, cdir=0, precision=8)
    Given an array of coefficients, p, return a nicely formatted 
    polynomial string in the form:
          anx^n + bn-1x^n-1 + ... + a1x + a0
    It removes trailing .0 if the coefficient is an integer,
    it only displays non-zero coefficients, 
    and if a coefficient is 1, it is left off.
    By default, cdir=0, the coefficient array is assumed to be in order
    of decending power (highest power first). If direction <> 0, then 
    the coefficient array is assumed to be in order of ascending power (lowest
    power first).
    The returned string will always print in decending power (highest order
    coefficients first).
    precision is used to control how may decimal places are included

