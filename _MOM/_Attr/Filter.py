# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Attr.Filter
#
# Purpose
#    Model query filters for MOM attributes
#
# Revision Dates
#    11-Nov-2011 (CT) Creation
#    12-Nov-2011 (CT) Move `AC` from `Table` to separate property
#    12-Nov-2011 (CT) Add `op_key` and use that as `Table` keys (`EQ`/`__eq__`)
#    14-Nov-2011 (CT) Change `Ckd.__getattr__` to support dotted attribute names
#    16-Nov-2011 (CT) Add translation markup (`_`)
#    17-Nov-2011 (CT) Add `NE` operator
#    17-Nov-2011 (CT) Add `_Type_` and `_M_Type_`
#    18-Nov-2011 (CT) Move `AC` into `_Table`; add `Op_Map`, `E_Type_Attr_Query`
#    20-Nov-2011 (CT) Add `Signatures` and `Sig_Key`
#    20-Nov-2011 (CT) Put `EQ`, `NE` into `Id_Entity.Table`
#    20-Nov-2011 (CT) Add `Children`
#    21-Nov-2011 (CT) Rename `_Type_.attr_name` to `._attr_name`
#    22-Nov-2011 (CT) Add `_Type_.as_json_cargo`
#    22-Nov-2011 (CT) Add `specialized`, streamline `as_json_cargo`
#    23-Nov-2011 (CT) Add `Base_Op_Table`, define `desc` for base operations
#     2-Dec-2011 (CT) Add `Boolean (_Type_)`
#     2-Dec-2011 (CT) Add `outer`, `Inner`, and `as_template_elem`
#     2-Dec-2011 (CT) Factor `_Composite_`, move parts of
#                     `_Type_.__getattr__` there
#     4-Dec-2011 (CT) Factor classes to `MOM.Attr.Querier`
#     4-Dec-2011 (CT) Change signature of `_Filter_.__init__` to `(querier)`
#     4-Dec-2011 (CT) Remove `prefix` from `__call__`, `a_query` and `query`
#     5-Dec-2011 (CT) Add and use `base_op_key`
#     6-Dec-2011 (CT) Change `_Filter_.__call__` to handle un-cookable
#                     `value == ""`
#     7-Dec-2011 (CT) Add guard for `value` to `_Date_.__call__`
#    ��revision-date�����
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _TFL.I18N             import _
from   _TFL.Regexp           import Regexp, re

import _TFL._Meta.Object
import _TFL.Filter

Q      = TFL.Attr_Query ()

class _M_Filter_ (TFL.Meta.Object.__class__) :
    """Meta class for Filter classes."""

    Base_Op_Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if not name.startswith ("_") :
            if not getattr (cls, "specialized", False) :
                cls.op_nam = name.lower ().replace ("_", "-")
            if cls.op_sym is None :
                cls.op_sym = cls.op_nam
            op_key = cls.op_fct
            if op_key.startswith ("__") :
                op_key = op_key.replace ("_", "").upper ()
            cls.op_key = op_key
            if op_key not in cls.Base_Op_Table :
                cls.Base_Op_Table [op_key] = cls
            if cls.base_op_key is None :
                cls.base_op_key = op_key
    # end def __init__

    def __str__ (cls) :
        return "<Attr.Filter %s [%s]>" % (cls.op_key, cls.op_sym)
    # end def __str__

# end class _M_Filter_

class _Filter_ (TFL.Meta.Object) :
    """Base class for attribute filters."""

    __metaclass__ = _M_Filter_

    op_fct        = None ### Must be redefined for subclasses or instances
    op_sym        = None ### Must be redefined for subclasses
    base_op_key   = None

    def __init__ (self, querier) :
        self.querier = querier
    # end def __init__

    def __call__ (self, value) :
        cooker = self.cooker
        if cooker is not None :
            try :
                value = cooker (value)
            except (ValueError, TypeError) :
                if value == "" :
                    value = None
                else :
                    return None
        return self.query (value)
    # end def __call__

    @TFL.Meta.Once_Property
    def attr (self) :
        return self.querier._attr
    # end def attr

    @TFL.Meta.Once_Property
    def attr_name (self) :
        return self.querier._attr_name
    # end def attr_name

    @TFL.Meta.Once_Property
    def cooker (self) :
        return self.querier._cooker
    # end def cooker

    @TFL.Meta.Once_Property
    def a_query (self) :
        return getattr (Q, self.querier._q_name)
    # end def a_query

    def query (self, value) :
        q = getattr (self.a_query, self.op_fct)
        return q (value)
    # end def query

    def __str__ (self) :
        return "<Attr.%s %s.%s [%s]>" % \
            (self.__class__.__name__, self.attr_name, self.op_key, self.op_sym)
    # end def __str__

# end class _Filter_

class _Composite_ (_Filter_) :
    """Base class for composite-attribute filters."""

    specialized = True

    def __call__ (self, value) :
        q      = self.querier
        E_Type = self.attr.E_Type
        def _gen () :
            for k, v in value.iteritems () :
                qk   = getattr (q,  k)
                qop  = getattr (qk, self.base_op_key)
                r    = qop     (v)
                if r is not None :
                    yield r
        qs = tuple (_gen ())
        if len (qs) > 1 :
            return Q.AND (* qs)
        elif qs :
            return qs [0]
    # end def __call__

# end class _Composite_

class _Date_ (_Filter_) :
    """Base class for date-attribute filters."""

    specialized = True

    pat = Regexp \
        ( r"^"
            r"(?P<year> [0-9]{4})"
            r"(?: [-/]"
              r"(?P<month> [0-9]{2})"
            r")?"
          r"[-/]?"
          r"$"
        , re.VERBOSE
        )

    def __call__ (self, value) :
        pat = self.pat
        if value and pat.match (value) :
            q    = self.a_query
            args = (int (pat.year), )
            if pat.month :
                args = (int (pat.month, 10), ) + args
                q    = q.D.MONTH
            else :
                q    = q.D.YEAR
            return q (* args)
        else :
            return self.__super.__call__ (value)
    # end def __call__

# end class _Date_

class _Id_Entity_ (_Composite_) :
    """Base class for entity-attribute filters."""

    specialized = True

    def __call__ (self, value) :
        if isinstance (value, dict) :
            return self.__super.__call__ (value)
        else :
            return self.query (value)
    # end def __call__

# end class _Id_Entity_

class _String_ (_Filter_) :
    """Base class for string-attribute filters."""

    def query (self, value) :
        aq = self.a_query
        q  = getattr (aq, self.op_fct) if value else aq.__eq__
        return q (value)
    # end def query

# end class _String_

class Contains (_String_) :
    """Attribute query filter for contains."""

    desc          = _ \
        ("Select entities where the attribute contains the specified value")
    op_fct        = _ ("CONTAINS")

# end class Contains

class Ends_With (_String_) :
    """Attribute query for ends-with."""

    desc          = _ \
        ( "Select entities where the attribute value ends "
          "with the specified value"
        )
    op_fct        = _ ("ENDSWITH")

# end class Ends_With

class Equal (_Filter_) :
    """Attribute query filter for equality."""

    desc          = _ \
        ("Select entities where the attribute is equal to the specified value")
    op_fct        = "__eq__"
    op_sym        = "=="

# end class Equal

class Greater_Equal (_Filter_) :
    """Attribute query filter for greater-equal."""

    desc          = _ \
        ( "Select entities where the attribute is greater than, "
          "or equal to, the specified value"
        )
    op_fct        = "__ge__"
    op_sym        = ">="

# end class Greater_Equal

class Greater_Than (_Filter_) :
    """Attribute query filter for greater-than."""

    desc          = _ \
        ( "Select entities where the attribute is greater than "
          "the specified value"
        )
    op_fct        = "__gt__"
    op_sym        = ">"

# end class Greater_Than

class Less_Equal (_Filter_) :
    """Attribute query filter for less-equal."""

    desc          = _ \
        ( "Select entities where the attribute is less than, "
          "or equal to, the specified value"
        )
    op_fct        = "__le__"
    op_sym        = "<="

# end class Less_Than

class Less_Than (_Filter_) :
    """Attribute query filter for less-than."""

    desc          = _ \
        ( "Select entities where the attribute is less than "
          "the specified value"
        )
    op_fct        = "__lt__"
    op_sym        = "<"

# end class Less_Than

class Not_Equal (_Filter_) :
    """Attribute query filter for in-equality."""

    desc          = _ \
        ( "Select entities where the attribute is not "
          "equal to the specified value"
        )
    op_fct        = "__ne__"
    op_sym        = "!="

# end class Not_Equal

class Starts_With (_String_) :
    """Attribute query for starts-with."""

    desc          = _ \
        ( "Select entities where the attribute value starts "
          "with the specified value"
        )
    op_fct        = _ ("STARTSWITH")

# end class Starts_With

class Auto_Complete (Equal) :
    """Attribute query filter for auto-completion."""

    op_sym        = "auto-complete"
    base_op_key   = "AC"

# end class Auto_Complete

class Auto_Complete_S (Starts_With) :
    """String-Attribute query filter for auto-completion."""

    op_sym        = "auto-complete"

# end class Auto_Complete

class Composite_Auto_Complete (Auto_Complete, _Composite_) :
    """Composite-Attribute query filter for auto-completion."""

# end class Composite_Auto_Complete

class Composite_Equal (Equal, _Composite_) :
    """Composite-Attribute query filter for equality."""

# end class Composite_Equal

class Composite_Greater_Equal (Greater_Equal, _Composite_) :
    """Composite-Attribute query filter for greater-equal."""

# end class Composite_Greater_Equal

class Composite_Greater_Than (Greater_Than, _Composite_) :
    """Composite-Attribute query filter for greater-than."""

# end class Composite_Greater_Than

class Composite_Less_Equal (Less_Equal, _Composite_) :
    """Composite-Attribute query filter for less-than."""

# end class Composite_Less_Equal

class Composite_Less_Than (Less_Than, _Composite_) :
    """Composite-Attribute query filter for less-equal."""

# end class Composite_Less_Than

class Composite_Not_Equal (Not_Equal, _Composite_) :
    """Composite-Attribute query filter for in-equality."""

# end class Composite_Not_Equal

class Date_Auto_Complete (Auto_Complete, _Date_) :
    """Date-Attribute query filter for auto-completion."""

# end class Date_Auto_Complete

class Date_Equal (Equal, _Date_) :
    """Date-Attribute query filter for equality."""

# end class Date_Equal

class Date_Greater_Equal (Greater_Equal, _Date_) :
    """Date-Attribute query filter for greater-equal."""

# end class Date_Greater_Equal

class Date_Greater_Than (Greater_Than, _Date_) :
    """Date-Attribute query filter for greater-than."""

# end class Date_Greater_Than

class Date_Less_Equal (Less_Equal, _Date_) :
    """Date-Attribute query filter for less-than."""

# end class Date_Less_Equal

class Date_Less_Than (Less_Than, _Date_) :
    """Date-Attribute query filter for less-equal."""

# end class Date_Less_Than

class Date_Not_Equal (Not_Equal, _Date_) :
    """Date-Attribute query filter for in-equality."""

# end class Date_Not_Equal

class Id_Entity_Auto_Complete (Auto_Complete, _Id_Entity_) :
    """Id_Entity-Attribute query filter for auto-completion."""

# end class Id_Entity_Auto_Complete

class Id_Entity_Equal (Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for equality."""

# end class Id_Entity_Equal

class Id_Entity_Greater_Equal (Greater_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-equal."""

# end class Id_Entity_Greater_Equal

class Id_Entity_Greater_Than (Greater_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-than."""

# end class Id_Entity_Greater_Than

class Id_Entity_Less_Equal (Less_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-than."""

# end class Id_Entity_Less_Equal

class Id_Entity_Less_Than (Less_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-equal."""

# end class Id_Entity_Less_Than

class Id_Entity_Not_Equal (Not_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for in-equality."""

# end class Id_Entity_Not_Equal

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
    MOM._Export ("Q")
### __END__ MOM.Attr.Filter
