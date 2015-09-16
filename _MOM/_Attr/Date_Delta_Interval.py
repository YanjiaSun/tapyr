# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Attr.Date_Delta_Interval
#
# Purpose
#    Composite attribute type for date interval specified as
#    (start, delta-or-finish)
#
# Revision Dates
#     3-Mar-2014 (CT) Creation
#    11-Mar-2014 (CT) Use `_Overrides`
#    11-Dec-2015 (CT) Use `attr_types_of_module`, not home-grown code
#    ««revision-date»»···
#--

from   __future__                  import division, print_function
from   __future__                  import absolute_import, unicode_literals

from   _CAL                        import CAL

from   _MOM.import_MOM             import *
from   _MOM.import_MOM             import _A_Composite_, _A_String_
from   _MOM._Attr.Date_Interval    import *

from   _TFL.I18N                   import _, _T, _Tn
from   _TFL.pyk                    import pyk

import _CAL.Delta

import datetime

class A_Date_or_Delta (A_Attr_Type) :
    """A date value or a date-delta value."""

    example        = "+2 years 3 months, 2 weeks -3 days"
    completer      = MOM.Attr.Completer_Spec  (4)
    output_format  = "%Y-%m-%d"
    typ            = _ ("Date")
    ui_length      = 48

    class Pickler (TFL.Meta.Object) :

        Type = _A_String_

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return attr_type.as_string (value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                return attr_type._from_string (cargo)
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, pyk.string_types) :
            try :
                value = soc._from_string (value)
            except ValueError :
                msg = "Date-or-delta expected, got %r" % (value, )
                raise MOM.Error.Attribute_Syntax (None, soc, value, msg)
        elif not isinstance (value, (datetime.date, CAL.Month_Delta)) :
            raise TypeError ("Date-or-delta expected, got %r" % (value, ))
        return value
    # end def cooked

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            if isinstance (value, datetime.date) :
                return pyk.text_type (value.strftime (soc._output_format ()))
            else :
                return str (value)
        return ""
    # end def as_string

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, s, obj = None, glob = {}, locl = {}) :
        s = s.strip ()
        if s :
            if s.startswith ("+") :
                result = CAL.Month_Delta.from_string (s)
            else :
                for f in A_Date.input_formats :
                    try :
                        result = time.strptime (s, f)
                    except ValueError :
                        pass
                    else :
                        result = datetime.date (result [0:3])
                        break
                else :
                    raise MOM.Error.Attribute_Syntax (obj, soc, s)
            return result
    # end def _from_string

# end class A_Date_or_Delta

class A_Date_Delta_Interval (A_Date_Interval) :
    """Date-or-delta interval (start, delta-or-finish)"""

    typ            = "Date_Delta_Interval"

    class _Attributes :

        def computed__finish (self, obj) :
            fod = obj.delta_or_finish
            if fod :
                if isinstance (fod, datetime.date) :
                    result = fod
                elif obj.start :
                    result = obj.start + fod
                return result
        # end def computed__finish

        _Overrides = dict \
            ( finish = dict
                ( kind             = Attr.Internal
                , Kind_Mixins      = (Attr.Computed_Set_Mixin, )
                , computed         = computed__finish
                , auto_up_depends  = ("delta_or_finish", "start")
                )
            )

        class delta_or_finish (A_Date_or_Delta) :
            """Length of interval or finish date."""

            kind               = Attr.Optional
            example            = "+2 years 3 months, 2 weeks -3 days"
            rank               = 2
            syntax             = _ \
                ( "A leading `+` indicates a length value; otherwise a date "
                  "is assumed."
                  "<br>"
                  "A length value can contain delta values for `years`, "
                  "`month`, `weeks`, and `days`. All units are optional, "
                  "but must occur in that sequence."
                  "<br>"
                  "Examples for valid length values:"
                  "<br>"
                  "    +2 years 3 months, 2 weeks -3 days"
                  "<br>"
                  "    +1 month, 15 days"
                  "<br>"
                  "    +2w3d"
                )

        # end class delta_or_finish

    # end class _Attributes

    class _Predicates :

        _Overrides = dict \
            ( finish_after_start = dict (kind = Pred.Region)
            )

    # end class _Predicates

# end class A_Date_Interval

class A_Date_Delta_Interval_N (A_Date_Delta_Interval) :
    """Date-or-delta interval (start [default: now], delta-or-finish)"""

    class _Attributes :

        _Overrides = dict \
            ( start  = dict
                ( Kind_Mixins      = (Attr.Sticky_Mixin, )
                , computed_default = A_Date.now
                )
            )

    # end class _Attributes

# end class A_Date_Interval

__attr_types = Attr.attr_types_of_module ()
__all__      = __attr_types

if __name__ != "__main__" :
    MOM.Attr._Export (* __attr_types)
### __END__ MOM.Attr.Date_Delta_Interval
