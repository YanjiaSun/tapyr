# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Math_Func
#
# Purpose
#    Augment standard math module by additional functions
#
# Revision Dates
#     2-Mar-1998 (CT)  Creation
#    25-Aug-1998 (CT)  `intersection' optimized (use hash-table instead of
#                      iterative comparison)
#    28-Jan-1999 (CT)  `intersection' moved to `predicate.py'
#    28-Jan-1999 (MG)  `greatest_common_divisor', `least_common_multiple',
#                      `gcd' and `lcm' added
#    15-Feb-2001 (CT)  `gcd' streamlined
#    15-Feb-2001 (CT)  `default' added to `greatest_common_divisor' and
#                      `least_common_multiple' and check for empty `seq' added
#                      to prevent IndexError
#     4-Dec-2001 (CT)  `p2_ceil` added
#    30-Aug-2002 (CT)  `p2_ceil` corrected (division by 8 is *not* reusable)
#    27-Feb-2004 (CT)  `average` and `standard_deviation` added
#     5-Apr-2004 (CT)  `p2_ceil` changed to return a number of the same type
#                      as passed as argument instead of a real
#    10-Dec-2004 (ABR) Corrected classic int division for `lcm`
#    14-Feb-2006 (CT)  Moved into package `TFL`
#    13-Oct-2006 (PGO) `linregress` added (very simple version)
#    16-Oct-2006 (CED) `linregress` filled with life,
#                      `coefficent_of_correlation` added, functions sorted
#    17-Oct-2006 (CED) s/linregress/linear_regression/,  implement robust
#                      regression
#    17-Oct-2006 (CED) Removed `coefficent_of_correlation`,  added `residuals`
#    20-Oct-2006 (CED) s/linear_regression/linear_regression_1/,
#                      `residuals` moved out
#    ��revision-date�����
#--

from   _TFL import TFL

from   math import *
import operator

_log2 = log (2)

def average (seq) :
    """Returns the average value of the elements in `seq`.

       >>> s = (1.28, 1.31, 1.29, 1.28, 1.30, 1.31, 1.27)
       >>> "%4.2f" % (average (s),)
       '1.29'
    """
    return float (sum (seq)) / len (seq)
# end def average

def log2  (x) :
    return log (x) / _log2
# end def log2

def gcd (a, b) :
    """Calculates the greates common devisor of `a' and  `b'"""
    a = abs (a)
    b = abs (b)
    if (a < b) :
        a, b = b, a
    while (b) :
        a, b = b, a % b
    return a or 1
# end def gcd

def greatest_common_divisor (seq, default = None) :
    """Calculates the greates common devisor of `seq'"""
    result = default
    if seq :
        result = seq [0]
        for i in seq [1:] :
            result = gcd (result, i)
    return result
# end def greatest_common_divisor

def lcm (a, b) :
    """Calculates the least common multiple of `a' and `b'"""
    return (a // gcd (a, b)) * b
# end def lcm

def least_common_multiple (seq, default = None) :
    """Calculates the least common multiple of `seq'"""
    result = default
    if seq :
        result = seq [0]
        for i in seq [1:] :
            result = lcm (result, i)
    return result
# end def least_common_multiple

def linear_regression_1 (xs, ys) :
    """Linear regression algorithm for 2-dimensional data
       (== 1 free variable).
       (see http://en.wikipedia.org/wiki/Linear_regression#Robust_regression)
       Returns offset and slope of a straight line approximating the
       data points given by `xs` and `ys`.
    """
    assert len (xs) == len (ys)
    n       = float (len (xs))
    sx      = sum (xs)
    sy      = sum (ys)
    sxx     = sum (x * x  for x    in xs)
    sxy     = sum (x * y  for x, y in zip (xs, ys))
    k       = (n*sxy - sx*sy) / (n*sxx - sx*sx)
    d       = (sy - k*sx) / n
    return d, x
# end def linear_regression

def p2_ceil (n) :
    """Return next larger power of 2 for `n`.

       >>> [p2_ceil (i) for i in range (1, 9)]
       [1, 2, 4, 4, 8, 8, 8, 8]
    """
    return n.__class__ (2 ** ceil (log2 (n)))
# end def p2_ceil

def standard_deviation_plain (seq) :
    """Returns the standard deviation (aka root mean square) of the elements
       in `seq`. Beware of numerical instabilities.

       >>> s = (1.28, 1.31, 1.29, 1.28, 1.30, 1.31, 1.27)
       >>> "%5.3f" % (standard_deviation_plain (s),)
       '0.016'
    """
    n    = len     (seq)
    mean = average (seq)
    return sqrt (sum (((mean - v) ** 2) for v in seq) / (n - 1))
# end def standard_deviation_plain

def standard_deviation (seq) :
    """Returns the standard deviation (aka root mean square) of the elements
       in `seq`. Beware numerical instabilities.

       >>> s = (1.28, 1.31, 1.29, 1.28, 1.30, 1.31, 1.27)
       >>> "%5.3f" % (standard_deviation (s),)
       '0.016'
    """
    n     = len (seq)
    a1    = sum (v * v for v in seq) * n
    a2    = sum (seq) ** 2
    return sqrt ((a1 - a2) / (n * (n - 1)))
# end def standard_deviation

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Math_Func
