# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
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
#    CAL.Ordinal
#
# Purpose
#    Support the use of ordinal numbers for weeks, months etc.
#
# Revision Dates
#     3-Jan-2007 (CT) Creation
#    11-Aug-2007 (CT) `Quarter` and doc-test added
#    ��revision-date�����
#--

"""
>>> from _CAL.Date import *
>>> d1 = Date (1958, 1, 30)
>>> d2 = Date (1960, 4, 11)
>>> d3 = Date (1959, 9, 26)
>>> d4 = Date (1997, 11, 16)
>>> d5 = Date (2007,  1, 25) ### week  4
>>> d6 = Date (2007,  4, 25) ### week 17
>>> d7 = Date (2007,  7,  4) ### week 27
>>> d8 = Date (2007, 12, 24) ### week 52
>>> for U in Month, Quarter, Week, Year :
...     print U.__name__
...     for d in (d1, d2, d3, d4, d5, d6, d7, d8) :
...         o = U.to_ordinal (d)
...         print "    %s %8d %s" % (d, o, U.to_date (o))
...
Month
    1958-01-30    23497 1958-01-01
    1960-04-11    23524 1960-04-01
    1959-09-26    23517 1959-09-01
    1997-11-16    23975 1997-11-01
    2007-01-25    24085 2007-01-01
    2007-04-25    24088 2007-04-01
    2007-07-04    24091 2007-07-01
    2007-12-24    24096 2008-12-01
Quarter
    1958-01-30     7833 1958-01-01
    1960-04-11     7842 1960-04-01
    1959-09-26     7839 1959-07-01
    1997-11-16     7992 1998-10-01
    2007-01-25     8029 2007-01-01
    2007-04-25     8030 2007-04-01
    2007-07-04     8031 2007-07-01
    2007-12-24     8032 2008-10-01
Week
    1958-01-30   102115 1958-01-27
    1960-04-11   102230 1960-04-11
    1959-09-26   102201 1959-09-21
    1997-11-16   104191 1997-11-10
    2007-01-25   104671 2007-01-22
    2007-04-25   104684 2007-04-23
    2007-07-04   104694 2007-07-02
    2007-12-24   104719 2007-12-24
Year
    1958-01-30     1958 1958-01-01
    1960-04-11     1960 1960-01-01
    1959-09-26     1959 1959-01-01
    1997-11-16     1997 1997-01-01
    2007-01-25     2007 2007-01-01
    2007-04-25     2007 2007-01-01
    2007-07-04     2007 2007-01-01
    2007-12-24     2007 2007-01-01
"""

from   _TFL                    import TFL
from   _CAL                    import CAL
import _CAL.Date
import _TFL._Meta.Object

class Month (TFL.Meta.Object) :
    """Ordinal numbers for months."""

    @classmethod
    def to_date (cls, mo) :
        """Return date corresponding to month ordinal `mo`."""
        y, m = divmod (mo, 12)
        return CAL.Date (y, m or 12, 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return month ordinal for date `d`."""
        return d.year * 12 + d.month
    # end def to_ordinal

# end class Month

class Quarter (TFL.Meta.Object) :
    """Ordinal numbers for quarters"""

    @classmethod
    def to_date (cls, qu) :
        """Return date corresponding to quarter ordinal `qu`."""
        y, q = divmod (qu, 4)
        return CAL.Date (y, ((q or 4) - 1) * 3 + 1, 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return quarter ordinal for date `d`."""
        return d.year * 4 + d.quarter
    # end def to_ordinal

# end class Quarter

class Week (TFL.Meta.Object) :
    """Ordinal numbers for weeks"""

    @classmethod
    def to_date (cls, wo) :
        """Return date corresponding to week ordinal `wo`."""
        return CAL.Date.from_ordinal (wo * 7 + 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return week ordinal for date `d`."""
        return d.wk_ordinal
    # end def to_ordinal

# end class Week

class Year (TFL.Meta.Object) :
    """Ordinal numbers for years."""

    @classmethod
    def to_date (cls, yo) :
        """Return date corresponding to year ordinal `yo`."""
        return CAL.Date (yo, 1, 1)
    # end def to_date

    @classmethod
    def to_ordinal (cls, d) :
        """Return year ordinal for date `d`."""
        return d.year
    # end def to_ordinal

# end class Year

if __name__ == "__main__" :
    CAL._Export_Module ()
### __END__ CAL.Ordinal
