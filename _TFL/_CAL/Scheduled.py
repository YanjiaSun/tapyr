# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CAL.Scheduled
#
# Purpose
#    Model a scheduled item (appointment, to-do, ...)
#
# Revision Dates
#    30-Oct-2004 (CT) Creation
#     2-Nov-2004 (CT) Creation continued
#    12-Dec-2004 (CT) Use `TFL.CAL.Formatter_Scope` instead of
#                         `TFL.Caller.Object_Scope`
#    12-Dec-2004 (CT) Attribute  `time` renamed to `start`
#    12-Dec-2004 (CT) Properties `time` and `finish` added
#    12-Dec-2004 (CT) Doctest added
#    12-Dec-2004 (CT) Default format added
#    12-Dec-2004 (CT) `__repr__` added
#    ��revision-date�����
#--

from   _TFL                    import TFL
import _TFL._CAL
import _TFL._CAL.Formatter_Scope
import _TFL._Meta.Object

class Scheduled (TFL.Meta.Object) :
    """Root class for all types of scheduled items

       >>> from _TFL._CAL.Date       import *
       >>> from _TFL._CAL.Delta      import *
       >>> from _TFL._CAL.Time       import *
       >>> s = Scheduled ( description = "First test"
       ...               , start       = Time       (16, 0, 0)
       ...               , duration    = Time_Delta ( 1, 30)
       ...               ).formatted ()
       >>> print s
       > 16:00-17:30   < First test
       >>> s = Scheduled ( description = "Second test"
       ...               , priority    = "A"
       ...               , start       = Time       (16, 0, 0)
       ...               ).formatted ()
       >>> print s
       > 16:00       A < Second test
       >>> s = Scheduled ( description = "Third test"
       ...               , priority    = "B"
       ...               , duration    = Time_Delta ( 1, 30)
       ...               ).formatted ()
       >>> print s
       >    1h 30m   B < Third test
    """

    prototype         = None
    attr_defaults     = dict \
        ( alarm       = None
        , deadline    = None
        , description = None
        , duration    = None
        , format      = "> %(time)-11s %(priority)1.1s < %(description)s"
        , kind        = None
        , location    = None
        , priority    = None
        , reminder    = None
        , start       = None
        , title       = None
        , x_attrs     = None
        )

    def _get_finish (self) :
        if self.start is not None and self.duration is not None :
            return self.start + self.duration
    # end def _get_finish

    def _get_time (self) :
        result = []
        sep    = "-"
        start  = self.start
        if start is not None :
            finish = self.finish
            fmt    = "%02.2d:%02.2d"
            result.append (fmt % (start.hour, start.minute))
            if finish is not None :
                result.append (fmt % (finish.hour, finish.minute))
        else :
            duration = self.duration
            if duration is not None :
                sep = " "
                result.append (" ")
                if duration.h :
                    result.append ("%2dh" % (duration.h, ))
                if duration.m :
                    result.append ("%2dm" % (duration.m, ))
        return sep.join (result)
    # end def _get_time

    finish            = property (_get_finish)
    time              = property (_get_time)

    def __init__ (self, ** kw) :
        for k, v in kw.iteritems () :
            if v is not None :
                setattr (self, k, v)
    # end def __init__

    def derived (self, ** kw) :
        return self.__class__ (prototype = self, ** kw)
    # end def derived

    def formatted (self, format = None) :
        if format is None :
            format = self.format
        if format is not None :
            return format % TFL.CAL.Formatter_Scope (self)
    # end def formatted

    def substantial_attributes (self) :
        for n, d in self.attr_defaults.iteritems () :
            v = getattr (self, n)
            if v is not d :
                yield n, v
    # end def substantial_attributes

    def __getattr__ (self, name) :
        if self.prototype is not None :
            return getattr (self.prototype, name)
        elif name in self.attr_defaults :
            return self.attr_defaults [name]
        raise AttributeError, name
    # end def __getattr__

    def __str__ (self) :
        return self.formatted ()
    # end def __str__

    def __repr__ (self) :
        cname  = "%s" % self.__class__.__name__
        attrs  = sorted (self.substantial_attributes ())
        if len (attrs) > 1 :
            format = "%s \\%s( %s%s)"
            a_fmt  = "%%-%ss = %%r" % (max ([len (n) for (n, v) in attrs]))
            sep    = "\n    "
        else :
            format = "%s %s(%s%s)"
            a_fmt  = "%s = %r"
            sep    = ""
        result = format % \
            ( cname
            , sep
            , (sep + ", ").join
                  ([a_fmt % (n, v) for (n, v) in attrs])
            , sep
            )
        return result
    # end def __repr__

# end class Scheduled

"""
from _TFL._CAL.Scheduled  import *
from _TFL._CAL.Date       import *
from _TFL._CAL.Delta      import *
from _TFL._CAL.Time       import *
Scheduled ()
Scheduled (start = Time (16, 0, 0))
Scheduled \
    ( description = "First test"
    , start       = Time       (16, 0, 0)
    , duration    = Time_Delta ( 1, 30)
    , format      =
          "> %(time)-11s %(priority)1.1s < %(description)s"
    )

print Scheduled \
    ( description = "First test"
    , start       = Time       (16, 0, 0)
    , format      =
          "> %(time)-11s %(priority)1.1s < %(description)s"
    ).formatted ()

"""
if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TFL.CAL.Scheduled
