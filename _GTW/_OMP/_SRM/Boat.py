# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.SRM.Boat
#
# Purpose
#    Model a sailboat
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#     5-May-2010 (CT) `sail_number` changed from `A_Int` to
#                     `A_Numeric_String` to allow autocompletion
#     7-May-2010 (CT) `sail_number` changed back to `A_Int` to fix sorting
#                     and set `needs_raw_value` to allow autocompletion
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `left`
#     9-Feb-2011 (CT) `Boat.left.ui_allow_new` set to `True`
#     2-May-2011 (CT) `sail_number_x` added
#    30-May-2011 (CT) `nation` changed from `Primary` to `Primary_Optional`
#     7-Sep-2011 (CT) `completer` added for `nation` and `sail_number`
#     9-Sep-2011 (CT) `completer` removed from `nation`
#    13-Sep-2011 (CT) `sail_number_x` changed from `Optional` to
#                     `Primary_Optional`
#    23-Sep-2011 (CT) `sail_number_x` and `sail_number` merged into a single
#                     attribute of type `A_String`, kind `Primary_Optional`
#     9-Nov-2011 (CT) Add cached attributes `sail_number_head` and `_tail`
#    17-Nov-2011 (CT) Split off `sail_number_x` again (to fix sorting)
#    17-Nov-2011 (CT) Redefine `ui_display_format` and `ui_display_sep`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    20-Jan-2012 (CT) Add `sail_number.max_value`
#     8-Sep-2012 (CT) Add `valid_sail_number_x`
#     8-Sep-2012 (CT) Set `sail_number_x.ignore_case` to `"upper"`
#    11-Sep-2012 (CT) Add add `sail_number` to `valid_sail_number_x`
#    11-Sep-2012 (CT) Fix typo introduced in last change
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

from   _GTW._OMP._SRM.Attr_Type import *

import _GTW._OMP._SRM.Boat_Class
import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Boat (_Ancestor_Essence) :
    """Boat of a specific boat-class."""

    ui_display_sep        = " "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Boat-class of boat."""

            role_type          = GTW.OMP.SRM.Boat_Class
            role_name          = "b_class"
            ui_name            = "Class"
            ui_allow_new       = True

        # end class left

        class nation (A_Nation) :
            """Country for which the boat is registered."""

            kind               = Attr.Primary_Optional
            example            = "AUT"

        # end class nation

        class sail_number (A_Int) :
            """Sail number of boat"""

            kind               = Attr.Primary_Optional
            example            = "2827"
            min_value          = 0
            max_value          = 999999
            needs_raw_value    = True
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class sail_number

        class sail_number_x (A_String) :
            """Sail number prefix of boat (e.g., "X", not the nation code!)."""

            kind               = Attr.Primary_Optional
            example            = "X"
            ignore_case        = "upper"
            max_length         = 8
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class sail_number_x

        ### Non-primary attributes

        class name (A_String) :
            """Name of sailboat."""

            kind               = Attr.Optional
            example            = "Albatross"
            max_length         = 48

        # end class name

        class sail_number_head (A_String) :
            """Non numeric head of `sail_number`, if any."""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("sail_number_x",)

            def computed (self, obj) :
                return obj.raw_attr ("sail_number_x")
            # end def computed

        # end class sail_number_head

        class sail_number_tail (A_String) :
            """Numeric tail of `sail_number`."""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("sail_number",)

            def computed (self, obj) :
                return obj.raw_attr ("sail_number")
            # end def computed

        # end class sail_number_tail

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_sail_number_x (Pred.Condition) :
            """`sail_number_x` must not repeat either `nation` or `sail_number`."""

            kind               = Pred.Object
            assertion          = \
              "sail_number_x not in (nation, str (sail_number))"
            attributes         = ("nation", "sail_number", "sail_number_x")

        # end class valid_sail_number_x

        class valid_vintage (Pred.Condition) :
            """`vintage` must not lie in the future."""

            kind               = Pred.Object
            assertion          = "vintage <= current_year"
            attributes         = ("vintage",)
            bindings           = dict \
                ( current_year = "datetime.datetime.now ().year"
                )

        # end class valid_vintage

    # end class _Predicates

    @property
    def ui_display_format (self) :
        cls  = self.__class__
        head = result = "%(left)s"
        tail = self.ui_display_sep.join \
            (   "%%(%s)s" % (a.name, )
            for a in (cls.nation, cls.sail_number_x, cls.sail_number)
            if  a.has_substance (self)
            )
        if tail :
            result = ", ".join ((head, tail))
        return result
    # end def ui_display_format

# end class Boat

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Boat


