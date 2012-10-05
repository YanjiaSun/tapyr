# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.MOM
#
# Purpose
#    Test for MOM meta object model
#
# Revision Dates
#    18-Oct-2009 (CT) Creation
#     4-Nov-2009 (CT) Creation continued
#     4-Nov-2009 (MG) `Beaver` and `Otter` added
#    23-Nov-2009 (CT) Creation continued..
#    24-Nov-2009 (CT) Creation continued...
#    25-Nov-2009 (CT) Creation continued....
#    27-Nov-2009 (CT) Creation continued.....
#    27-Nov-2009 (MG) Order of test cases changed, use `list` operator in
#                     some tests
#     4-Dec-2009 (MG) Tests adopted to use real database back end
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    18-Jan-2010 (MG) Tests fixed (`Invalid_Attribute` now has a different
#                     error message)
#    21-Jan-2010 (CT) `Primary_Optional` added
#    29-Jan-2010 (MG) Tests for scope rollback added/enhanced
#    29-Jan-2010 (MG) Tests for pid_from_lid/pid_as_lid/obj.lid/ added
#     6-Feb-2010 (MG) Use `t4` for new `auto_up_depends` test instance of
#                     `t1` (because all other traps are are already destroyed)
#     8-Feb-2010 (CT) Doctest for `t4.up_ex` corrected
#    14-Feb-2010 (MG) Fixed doctest after fixing `Entity._record_iter` (which
#                     introducted a new change object)
#    18-Feb-2010 (CT) `Rodent_is_sick` added to test unary links
#    19-Feb-2010 (MG) Test for auto cached links added
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/
#    17-May-2010 (CT) Test for `scope.migrate` added
#    17-Aug-2010 (CT) Use A_Float instead of A_Decimal to avoid sqlite warning
#     1-Sep-2010 (CT) Tests for `Q.attr`, `Q.attrs`, and `Q.set` added
#    28-Sep-2010 (CT) Adapted to change of `epk_raw`
#    20-Dec-2010 (CT) Python 2.7 compatibility
#     8-Feb-2011 (CT) s/Required/Necessary/, s/Mandatory/Required/
#    18-Nov-2011 (CT) Add `formatted1` to get rid of `u` prefixes
#    15-Apr-2012 (CT) Adapt to changes of `MOM.Error`
#    16-Apr-2012 (CT) Adapt to more changes of `MOM.Error`
#    14-May-2012 (CT) Add `Supertrap.weights` to test `A_Float_Interval`
#    14-May-2012 (CT) Factor function `show_children` to module `MOM.inspect`
#    14-May-2012 (CT) Remove prefix `u` from strings,
#                     import `unicode_literals` from `__future__` instead
#     8-Jun-2012 (CT) Add test for `query_changes` of `type_name`
#     3-Aug-2012 (CT) Use `Ref_Req_Map`, not `link_map`
#    ��revision-date�����
#--

from   __future__  import unicode_literals

from   _MOM.import_MOM            import *
from   _MOM._Attr.Date_Interval   import *
from   _MOM._Attr.Number_Interval import A_Float_Interval
from   _MOM.inspect               import show_children
from   _MOM.Product_Version       import Product_Version, IV_Number
from   _TFL.Package_Namespace     import Derived_Package_Namespace
from   _TFL                       import sos

BMT = Derived_Package_Namespace (parent = MOM, name = "_BMT")

Version = Product_Version \
    ( productid           = "Better Mouse Trap"
    , productnick         = "BMT"
    , productdesc         = "Example application for MOM meta object model"
    , date                = "18-Dec-2009"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = "Christian Tanzer, Martin Gl�ck"
    , copyright_start     = 2009
    , db_version          = IV_Number
        ( "db_version"
        , ("Better Mouse Trap", )
        , ("Better Mouse Trap", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".bmt"
        )
    , script_api_version  = IV_Number
        ( "script_api_version"
        , ("Better Mouse Trap", )
        , ("Example Client 1", "Example Client 2")
        , program_version = 1
        , comp_min        = 0
        )
    )

_Ancestor_Essence = MOM.Object

class Location (_Ancestor_Essence) :
    """Model a location of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class lon (A_Float) :
            """Longitude """

            kind       = Attr.Primary
            rank       = 1
            min_value  = -180.0
            max_value  = +180.0
            ui_name    = "Longitude"

        # end class lon

        class lat (A_Float) :
            """Latitude"""

            kind       = Attr.Primary
            rank       = 2
            min_value  = -90.0
            max_value  = +90.0
            ui_name    = "Latitude"

        # end class lat

    # end class _Attributes

# end class Location

_Ancestor_Essence = MOM.Object

class Person (_Ancestor_Essence) :
    """Model a person of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class last_name (A_String) :
            """Last name of person"""

            kind        = Attr.Primary
            ignore_case = True
            rank        = 1

        # end class last_name

        class first_name (A_String) :
            """First name of person"""

            kind        = Attr.Primary
            ignore_case = True
            rank        = 2
            ui_name     = "First name"

        # end class first_name

        class middle_name (A_String) :
            """Middle name of person"""

            kind        = Attr.Primary_Optional
            ignore_case = True
            max_length  = 5
            rank        = 1
            ui_name     = "Middle name"

        # end class middle_name

    # end class _Attributes

# end class Person

_Ancestor_Essence = MOM.Named_Object

class Rodent (_Ancestor_Essence) :
    """Model a rodent of the Better Mouse Trap application."""

    PNS    = BMT

    default_child = "BMT.Rat"

    is_partial    = True
    is_relevant   = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        class color (A_String) :
            """Color of the rodent"""

            kind     = Attr.Optional

        # end class color

        class weight (A_Float) :
            """Weight of the rodent"""

            kind     = Attr.Necessary
            check    = ("value > 0", )

        # end class weight

    # end class _Attributes

# end class Rodent

_Ancestor_Essence = Rodent

class Mouse (_Ancestor_Essence) :
    """Model a mouse of the Better Mouse Trap application."""

# end class Mouse

_Ancestor_Essence = Rodent

class Rat (_Ancestor_Essence) :
    """Model a rat of the Better Mouse Trap application."""

# end class Rat

_Ancestor_Essence = Mouse

class Beaver (_Ancestor_Essence) :
    """Model a beaver of the Better Mouse Trap application."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        class region (A_String) :
            """In which are lives the beaver"""

            kind     = Attr.Optional

        # end class region

    # end class _Attributes

# end class Beaver

_Ancestor_Essence = Beaver

class Otter (_Ancestor_Essence) :

    class _Attributes (_Ancestor_Essence._Attributes) :

        class river (A_String) :

            kind       = Attr.Optional
            max_length = 20

        # end class river

    # end class _Attributes

# end class Otter

_Ancestor_Essence = MOM.Named_Object

class Trap (_Ancestor_Essence) :
    """Model a trap of the Better Mouse Trap application."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        class max_weight (A_Float) :
            """Maximum weight of rodent the trap can hold"""

            kind     = Attr.Optional
            check    = ("value > 0", )
            ui_name  = "Maximum weight"

        # end class max_weight

        class serial_no (A_Int) :
            """Serial number of the trap"""

            kind     = Attr.Primary
            ui_name  = "Serial number"

        # end class serial_no

        class up_ex (A_Float) :
            """Example for an attribute that depends on other
               attributes and is automatically changed whenever one of
               those changes.
            """

            kind               = Attr.Cached
            auto_up_depends    = ("max_weight", "serial_no")

            def computed (self, obj) :
                if obj.max_weight :
                    return obj.max_weight * obj.serial_no
            # end def computed

        # end class up_ex

        class up_ex_q (A_Float) :
            """Example for a query attribute that is recomputed
               whenever one of the attributes it depends on changes.
            """

            kind               = Attr.Query
            query              = Q.max_weight * Q.serial_no

            auto_up_depends    = ("max_weight", "serial_no")

        # end class up_ex_q

    # end class _Attributes

# end class Trap

_Ancestor_Essence = Trap

class Supertrap (_Ancestor_Essence) :
    """An enormously improved Trap."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class weights (A_Float_Interval) :
            """Range of weights this trap can safely hold"""

            kind               = Attr.Necessary

        # end class weights

    # end class _Attributes

# end class Supertrap

_Ancestor_Essence = MOM.Link1

class Rodent_is_sick (_Ancestor_Essence) :
    """Model the sickness of a rodent."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Rodent that is sick"""

            role_type     = Rodent
            auto_cache    = "sickness"

        # end class left

        class sick_leave (A_Date_Interval) :
            """Duration of sick leave"""

            kind               = Attr.Primary

        # end class sick_leave

        class fever (A_Float) :
            """Highest temperature during the sickness"""

            kind               = Attr.Optional

        # end class fever
    # end class _Attributes

# end class Rodent_is_sick

_Ancestor_Essence = MOM.Link2

class Rodent_in_Trap (_Ancestor_Essence) :
    """Model a rodent caught in a trap."""

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Rodent caught in Trap."""

            role_type     = Rodent
            max_links     = 1
            auto_cache    = "catch"

        # end class left

        class right (_Ancestor.right) :
            """Trap that caught a rodent."""

            role_type     = Trap
            max_links     = 1
            auto_cache    = "catcher"

        # end class right

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        class valid_weight (Pred.Condition) :
            """Weight of `rodent` must not exceed `max_weight` of `trap`."""

            kind          = Pred.System
            assertion     = "rodent.weight <= trap.max_weight"
            attributes    = ("rodent.weight", "trap.max_weight")

        # end class valid_weight

    # end class _Predicates


# end class Rodent_in_Trap

_Ancestor_Essence = MOM.Link2

class Person_owns_Trap (_Ancestor_Essence) :

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Person owning the Trap."""

            role_name     = "owner"
            role_type     = Person
            auto_cache    = True

        # end class left

        class right (_Ancestor.right) :
            """Trap owned by person."""

            role_type     = Trap
            max_links     = 1
            auto_cache    = True

        # end class right

        class price (A_Float) :
            kind          = Attr.Optional
            default       = 42.0
        # end class price

    # end class _Attributes

# end class Person_owns_Trap

_Ancestor_Essence = MOM.Link3

class Person_sets_Trap_at_Location (_Ancestor_Essence) :

    PNS = BMT

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Person setting a trap."""

            role_type     = Person
            auto_cache    = MOM.Role_Cacher \
                ( attr_name       = "setter"
                , other_role_name = "middle"
                )

        # end class left

        class middle (_Ancestor.middle) :

            role_type     = Trap
            max_links     = 1

        # end class middle

        class right (_Ancestor.right) :
            """Location where a trap is set."""

            role_type     = Location
            auto_cache    = MOM.Role_Cacher (other_role_name = "middle")

        # end class right

    # end class _Attributes

# end class Person_sets_Trap_at_Location

def show (e) :
    if isinstance (e, (list, TFL._Q_Result_)) :
        print "[%s]" % (", ".join (str (x) for x in e), )
    else :
        print str (e)
# end def show

### All classes defining `__getslice__` have been changed to be
### compatible to Python 3.x by changing `__getitem__` to deal with
### slices
###
### Unfortunately, in Python 2.x `__getslice__` is still necessary and
### code like::
###
###     self.kill_callback [:]
###
### triggers the warning::
###
### DeprecationWarning: in 3.x, __getslice__ has been removed; use __getitem__
###
import warnings
warnings.filterwarnings \
    ( "ignore", "in 3.x, __getslice__ has been removed; use __getitem__")
if 0 :
    warnings.filterwarnings \
        ( "error",  "comparing unequal types not supported in 3.x")

### Because the example classes are all defined here and not in their
### own package namespace, we'll fake it
BMT._Export ("*", "Version")

NL = chr (10)

### �text�

dt_form = \
"""
How to define and use essential object models
==============================================

Using `MOM`, an essential object model is specified by deriving
classes from :class:`MOM.Object<_MOM.Object.Object>` or from one of
the arity-specific descendants of :class:`MOM.Link<_MOM.Link.Link>`.

Each essential class must be defined inside a
:class:`TFL.Package_Namespace<_TFL.Package_Namespace.Package_Namespace>`
and the class definition must contain an explicit or inherited
reference :attr:`PNS<_MOM.Entity.PNS>` to that package
namespace.

Normally, each essential class is defined in a module of its own. In
some cases, a single module might define more than one essential
class.

The module `_MOM.import_MOM` provides all classes necessary to define
essential object or link types and is meant to be imported like::

    >>> from _MOM.import_MOM import *

An essential class as defined by its module isn't usable before an
app-type is created.

    >>> BMT.Person
    <class 'BMT.Person' [Spec Essence]>
    >>> BMT.Rodent
    <class 'BMT.Rodent' [Spec Essence]>
    >>> BMT.Beaver
    <class 'BMT.Beaver' [Spec Essence]>
    >>> BMT.Person_owns_Trap
    <class 'BMT.Person_owns_Trap' [Spec Essence]>
    >>> BMT.Person.last_name
    Traceback (most recent call last):
        ...
    AttributeError: type object 'Person' has no attribute 'last_name'


Application type
----------------

Before an essential object model can be used, the
:class:`application type<_MOM.App_Type.App_Type>` and at least one
:class:`derived application type<_MOM.App_Type._App_Type_D_>` must be
defined:

    >>> %(import_EMS)s as EMS
    >>> %(import_DBW)s as DBW
    >>> try :
    ...   apt = MOM.App_Type ("BMT", BMT).Derived (EMS, DBW)
    ... except Exception as exc :
    ...   import traceback; traceback.print_exc ()
    ...   import os; os.abort ()

Creating a derived app-type replaces the specification of the
essential classes with bare essential classes:

    >>> BMT.Person
    <class 'BMT.Person' [Bare Essence]>
    >>> BMT.Rodent
    <class 'BMT.Rodent' [Bare Essence]>
    >>> BMT.Beaver
    <class 'BMT.Beaver' [Bare Essence]>
    >>> BMT.Person_owns_Trap
    <class 'BMT.Person_owns_Trap' [Bare Essence]>

and derives an app-type specific entity-type for each of the essential
classes:

    >>> ET_Entity    = apt.entity_type ("MOM.Entity")
    >>> ET_Id_Entity = apt.entity_type ("MOM.Id_Entity")
    >>> ET_Named_Obj = apt.entity_type ("MOM.Named_Object")
    >>> ET_Person    = apt.entity_type ("BMT.Person")
    >>> ET_Mouse     = apt ["BMT.Mouse"]
    >>> ET_Rat       = apt ["BMT.Rat"]
    >>> ET_Rodent    = apt ["BMT.Rodent"]
    >>> ET_Trap      = apt ["BMT.Trap"]
    >>> ET_Supertrap = apt ["BMT.Supertrap"]

For each `entity_type` with a unique :attr:`epk_sig`, the meta
machinery automatically creates methods `epkified_ckd` and
`epkified_raw` matching the `epk_sig`. These auto-generated methods
are used by `__init__` to ensure that the required parameters are
passed for the :ref:`essential primary keys<essential-primary-keys>`.

    >>> for et in apt._T_Extension :
    ...   if et.epk_sig and "epkified_ckd" in et.__dict__ :
    ...     print "***", et.type_name, "***", et.epk_sig
    ...     print et.epkified_ckd.source_code.rstrip ()
    ...     print et.epkified_raw.source_code.rstrip ()
    ...
    *** MOM.Link *** ('left',)
    def epkified_ckd (cls, left, ** kw) :
        return (left,), kw
    def epkified_raw (cls, left, ** kw) :
        return (left,), kw
    *** MOM.Link1 *** ('left',)
    def epkified_ckd (cls, left, ** kw) :
        return (left,), kw
    def epkified_raw (cls, left, ** kw) :
        return (left,), kw
    *** MOM._MOM_Link_n_ *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** MOM.Link2 *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** MOM.Link2_Ordered *** ('left', 'right', 'seq_no')
    def epkified_ckd (cls, left, right, seq_no, ** kw) :
        return (left, right, seq_no), kw
    def epkified_raw (cls, left, right, seq_no, ** kw) :
        return (left, right, seq_no), kw
    *** MOM.Link3 *** ('left', 'middle', 'right')
    def epkified_ckd (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    def epkified_raw (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    *** MOM.Named_Object *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Location *** ('lon', 'lat')
    def epkified_ckd (cls, lon, lat, ** kw) :
        return (lon, lat), kw
    def epkified_raw (cls, lon, lat, ** kw) :
        return (lon, lat), kw
    *** BMT.Person *** ('last_name', 'first_name', 'middle_name')
    def epkified_ckd (cls, last_name, first_name, middle_name = u'', ** kw) :
        return (last_name, first_name, middle_name), kw
    def epkified_raw (cls, last_name, first_name, middle_name = u'', ** kw) :
        return (last_name, first_name, middle_name), kw
    *** BMT.Rodent *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Mouse *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Rat *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Beaver *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Otter *** ('name',)
    def epkified_ckd (cls, name, ** kw) :
        return (name,), kw
    def epkified_raw (cls, name, ** kw) :
        return (name,), kw
    *** BMT.Trap *** ('name', 'serial_no')
    def epkified_ckd (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    def epkified_raw (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    *** BMT.Supertrap *** ('name', 'serial_no')
    def epkified_ckd (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    def epkified_raw (cls, name, serial_no, ** kw) :
        return (name, serial_no), kw
    *** BMT.Rodent_is_sick *** ('left', 'sick_leave')
    def epkified_ckd (cls, left, sick_leave, ** kw) :
        return (left, sick_leave), kw
    def epkified_raw (cls, left, sick_leave, ** kw) :
        return (left, sick_leave), kw
    *** BMT.Rodent_in_Trap *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** BMT.Person_owns_Trap *** ('left', 'right')
    def epkified_ckd (cls, left, right, ** kw) :
        return (left, right), kw
    def epkified_raw (cls, left, right, ** kw) :
        return (left, right), kw
    *** BMT.Person_sets_Trap_at_Location *** ('left', 'middle', 'right')
    def epkified_ckd (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw
    def epkified_raw (cls, left, middle, right, ** kw) :
        return (left, middle, right), kw

Each entity_type knows about its children:

    >>> for et in apt._T_Extension :
    ...   if et.children :
    ...     print et.type_name
    ...     print "   ", sorted (et.children)
    MOM.Entity
        ['MOM.An_Entity', 'MOM.Id_Entity']
    MOM.An_Entity
        ['MOM.Date_Interval', 'MOM._Interval_']
    MOM.Id_Entity
        ['MOM.Link', 'MOM.Object']
    MOM.Link
        ['MOM.Link1', 'MOM._MOM_Link_n_']
    MOM.Link1
        ['BMT.Rodent_is_sick']
    MOM._MOM_Link_n_
        ['MOM.Link2', 'MOM.Link3']
    MOM.Link2
        ['BMT.Person_owns_Trap', 'BMT.Rodent_in_Trap', 'MOM.Link2_Ordered']
    MOM.Link3
        ['BMT.Person_sets_Trap_at_Location']
    MOM.Object
        ['BMT.Location', 'BMT.Person', 'MOM.Named_Object']
    MOM.Named_Object
        ['BMT.Rodent', 'BMT.Trap']
    MOM.Date_Interval
        ['MOM.Date_Interval_C', 'MOM.Date_Interval_N']
    MOM._Interval_
        ['MOM.Float_Interval', 'MOM.Frequency_Interval']
    BMT.Rodent
        ['BMT.Mouse', 'BMT.Rat']
    BMT.Mouse
        ['BMT.Beaver']
    BMT.Beaver
        ['BMT.Otter']
    BMT.Trap
        ['BMT.Supertrap']

    >>> for et in apt._T_Extension :
    ...   if et.children and et.children != et.children_np :
    ...     print et.type_name
    ...     print "   ", sorted (et.children)
    ...     print "   ", sorted (et.children_np)
    MOM.Entity
        ['MOM.An_Entity', 'MOM.Id_Entity']
        ['BMT.Location', 'BMT.Mouse', 'BMT.Person', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rat', 'BMT.Rodent_in_Trap', 'BMT.Rodent_is_sick', 'BMT.Trap', 'MOM.Date_Interval', 'MOM._Interval_']
    MOM.Id_Entity
        ['MOM.Link', 'MOM.Object']
        ['BMT.Location', 'BMT.Mouse', 'BMT.Person', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rat', 'BMT.Rodent_in_Trap', 'BMT.Rodent_is_sick', 'BMT.Trap']
    MOM.Link
        ['MOM.Link1', 'MOM._MOM_Link_n_']
        ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent_in_Trap', 'BMT.Rodent_is_sick']
    MOM._MOM_Link_n_
        ['MOM.Link2', 'MOM.Link3']
        ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent_in_Trap']
    MOM.Link2
        ['BMT.Person_owns_Trap', 'BMT.Rodent_in_Trap', 'MOM.Link2_Ordered']
        ['BMT.Person_owns_Trap', 'BMT.Rodent_in_Trap']
    MOM.Object
        ['BMT.Location', 'BMT.Person', 'MOM.Named_Object']
        ['BMT.Location', 'BMT.Mouse', 'BMT.Person', 'BMT.Rat', 'BMT.Trap']
    MOM.Named_Object
        ['BMT.Rodent', 'BMT.Trap']
        ['BMT.Mouse', 'BMT.Rat', 'BMT.Trap']


The app-type specific entity-types are ready to be used by
:class:`scopes<_MOM.Scope.Scope>` and their
:mod:`etype managers<_MOM.E_Type_Manager>`:

    >>> ET_Person
    <class 'BMT.Person' [BMT__Hash__HPS]>
    >>> ET_Person.Essence
    <class 'BMT.Person' [Bare Essence]>
    >>> ET_Person.E_Spec
    <class 'BMT.Person' [Spec Essence]>
    >>> ET_Person.primary
    [String `last_name`, String `first_name`, String `middle_name`]
    >>> [attr.__class__.__name__ for attr in ET_Person.primary]
    ['Primary__Raw_Value', 'Primary__Raw_Value', 'Primary_Optional__Raw_Value']
    >>> ET_Person.necessary
    []
    >>> ET_Person.optional
    []

    >>> ET_Mouse.primary
    [Name `name`]
    >>> ET_Mouse.necessary
    [Float `weight`]
    >>> ET_Mouse.optional
    [String `color`]
    >>> sorted (ET_Mouse.attributes.itervalues (), key = TFL.Getter.name)
    [Blob `FO`, Cached_Role `catcher`, String `color`, Date-Time `creation_date`, Boolean `electric`, Int `is_used`, Date-Time `last_changed`, Int `last_cid`, Name `name`, Cached_Role_Set `sickness`, String `ui_display`, Float `weight`, Boolean `x_locked`]

    >>> ET_Person.last_name.name, ET_Person.last_name.ui_name
    ('last_name', u'Last name')
    >>> sorted (ET_Person._Attributes._own_names)
    ['first_name', 'last_name', 'middle_name', 'traps', 'ui_display']
    >>> ET_Mouse.color.name, ET_Mouse.color.ui_name
    ('color', u'Color')

    >>> sorted (ET_Trap._Attributes._own_names)
    ['catch', 'location', 'max_weight', 'owner', 'serial_no', 'setter', 'ui_display', 'up_ex', 'up_ex_q']
    >>> sorted (ET_Supertrap._Attributes._own_names)
    ['ui_display', 'weights']
    >>> sorted (ET_Trap._Attributes._names)
    ['FO', 'catch', 'creation_date', 'electric', 'is_used', 'last_changed', 'last_cid', 'location', 'max_weight', 'name', 'owner', 'serial_no', 'setter', 'ui_display', 'up_ex', 'up_ex_q', 'x_locked']
    >>> sorted (ET_Supertrap._Attributes._names)
    ['FO', 'catch', 'creation_date', 'electric', 'is_used', 'last_changed', 'last_cid', 'location', 'max_weight', 'name', 'owner', 'serial_no', 'setter', 'ui_display', 'up_ex', 'up_ex_q', 'weights', 'x_locked']
    >>> sorted (ET_Trap.attributes.itervalues (), key = TFL.Getter.name)
    [Blob `FO`, Cached_Role `catch`, Date-Time `creation_date`, Boolean `electric`, Int `is_used`, Date-Time `last_changed`, Int `last_cid`, Cached_Role `location`, Float `max_weight`, Name `name`, Cached_Role `owner`, Int `serial_no`, Cached_Role `setter`, String `ui_display`, Float `up_ex`, Float `up_ex_q`, Boolean `x_locked`]
    >>> sorted (ET_Supertrap.attributes.itervalues (), key = TFL.Getter.name)
    [Blob `FO`, Cached_Role `catch`, Date-Time `creation_date`, Boolean `electric`, Int `is_used`, Date-Time `last_changed`, Int `last_cid`, Cached_Role `location`, Float `max_weight`, Name `name`, Cached_Role `owner`, Int `serial_no`, Cached_Role `setter`, String `ui_display`, Float `up_ex`, Float `up_ex_q`, Float_Interval `weights`, Boolean `x_locked`]

    >>> print formatted1 (sorted (ET_Id_Entity.relevant_roots))
    ['BMT.Location', 'BMT.Person', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent', 'BMT.Rodent_in_Trap', 'BMT.Rodent_is_sick', 'BMT.Trap']
    >>> ET_Person.relevant_root
    <class 'BMT.Person' [BMT__Hash__HPS]>
    >>> ET_Rodent.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__HPS]>
    >>> ET_Mouse.relevant_root
    <class 'BMT.Rodent' [BMT__Hash__HPS]>

    >>> sorted (ET_Person.children)
    []
    >>> print formatted1 (sorted (ET_Rodent.children))
    ['BMT.Mouse', 'BMT.Rat']
    >>> sorted (ET_Rodent.children.itervalues (), key = TFL.Getter.type_name)
    [<class 'BMT.Mouse' [BMT__Hash__HPS]>, <class 'BMT.Rat' [BMT__Hash__HPS]>]
    >>> sorted (ET_Rat.children)
    []

    >>> print formatted1 (sorted (apt.etypes))
    ['BMT.Beaver', 'BMT.Location', 'BMT.Mouse', 'BMT.Otter', 'BMT.Person', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rat', 'BMT.Rodent', 'BMT.Rodent_in_Trap', 'BMT.Rodent_is_sick', 'BMT.Supertrap', 'BMT.Trap', 'MOM.An_Entity', 'MOM.Date_Interval', 'MOM.Date_Interval_C', 'MOM.Date_Interval_N', 'MOM.Entity', 'MOM.Float_Interval', 'MOM.Frequency_Interval', 'MOM.Id_Entity', 'MOM.Link', 'MOM.Link1', 'MOM.Link2', 'MOM.Link2_Ordered', 'MOM.Link3', 'MOM.Named_Object', 'MOM.Object', 'MOM._Interval_', 'MOM._MOM_Link_n_']
    >>> print formatted1 ([t.type_name for t in apt._T_Extension])
    ['MOM.Entity', 'MOM.An_Entity', 'MOM.Id_Entity', 'MOM.Link', 'MOM.Link1', 'MOM._MOM_Link_n_', 'MOM.Link2', 'MOM.Link2_Ordered', 'MOM.Link3', 'MOM.Object', 'MOM.Named_Object', 'MOM.Date_Interval', 'MOM.Date_Interval_C', 'MOM.Date_Interval_N', 'MOM._Interval_', 'MOM.Float_Interval', 'MOM.Frequency_Interval', 'BMT.Location', 'BMT.Person', 'BMT.Rodent', 'BMT.Mouse', 'BMT.Rat', 'BMT.Beaver', 'BMT.Otter', 'BMT.Trap', 'BMT.Supertrap', 'BMT.Rodent_is_sick', 'BMT.Rodent_in_Trap', 'BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location']
    >>> for t in apt._T_Extension [2:] :
    ...     print "%%-35s %%s" %% (t.type_name, t.epk_sig)
    MOM.Id_Entity                       ()
    MOM.Link                            ('left',)
    MOM.Link1                           ('left',)
    MOM._MOM_Link_n_                    ('left', 'right')
    MOM.Link2                           ('left', 'right')
    MOM.Link2_Ordered                   ('left', 'right', 'seq_no')
    MOM.Link3                           ('left', 'middle', 'right')
    MOM.Object                          ()
    MOM.Named_Object                    ('name',)
    MOM.Date_Interval                   ()
    MOM.Date_Interval_C                 ()
    MOM.Date_Interval_N                 ()
    MOM._Interval_                      ()
    MOM.Float_Interval                  ()
    MOM.Frequency_Interval              ()
    BMT.Location                        ('lon', 'lat')
    BMT.Person                          ('last_name', 'first_name', 'middle_name')
    BMT.Rodent                          ('name',)
    BMT.Mouse                           ('name',)
    BMT.Rat                             ('name',)
    BMT.Beaver                          ('name',)
    BMT.Otter                           ('name',)
    BMT.Trap                            ('name', 'serial_no')
    BMT.Supertrap                       ('name', 'serial_no')
    BMT.Rodent_is_sick                  ('left', 'sick_leave')
    BMT.Rodent_in_Trap                  ('left', 'right')
    BMT.Person_owns_Trap                ('left', 'right')
    BMT.Person_sets_Trap_at_Location    ('left', 'middle', 'right')

    >>> for t in apt._T_Extension [2:] :
    ...     print "%%s%%s    %%s" %% (t.type_name, NL, t.sorted_by.criteria)
    MOM.Id_Entity
        ('tn_pid',)
    MOM.Link
        ('left',)
    MOM.Link1
        ('left',)
    MOM._MOM_Link_n_
        ('left', 'right')
    MOM.Link2
        ('left', 'right')
    MOM.Link2_Ordered
        ('left', 'right', 'seq_no')
    MOM.Link3
        ('left', 'middle', 'right')
    MOM.Object
        ('tn_pid',)
    MOM.Named_Object
        ('name',)
    MOM.Date_Interval
        ('start', 'finish')
    MOM.Date_Interval_C
        ('start', 'finish')
    MOM.Date_Interval_N
        ('start', 'finish')
    MOM._Interval_
        ('lower', 'upper')
    MOM.Float_Interval
        (u'lower', u'upper')
    MOM.Frequency_Interval
        (u'lower', u'upper')
    BMT.Location
        ('lon', 'lat')
    BMT.Person
        ('last_name', 'first_name', 'middle_name')
    BMT.Rodent
        ('name',)
    BMT.Mouse
        ('name',)
    BMT.Rat
        ('name',)
    BMT.Beaver
        ('name',)
    BMT.Otter
        ('name',)
    BMT.Trap
        ('name', 'serial_no')
    BMT.Supertrap
        ('name', 'serial_no')
    BMT.Rodent_is_sick
        ('left.name', 'sick_leave.start', 'sick_leave.finish')
    BMT.Rodent_in_Trap
        ('left.name', 'right.name', 'right.serial_no')
    BMT.Person_owns_Trap
        ('left.last_name', 'left.first_name', 'left.middle_name', 'right.name', 'right.serial_no')
    BMT.Person_sets_Trap_at_Location
        ('left.last_name', 'left.first_name', 'left.middle_name', 'middle.name', 'middle.serial_no', 'right.lon', 'right.lat')

    >>> show_ref_map (ET_Person, "Ref_Req_Map")
    BMT.Person
        ('BMT.Person_owns_Trap', ['left'])
        ('BMT.Person_sets_Trap_at_Location', ['left'])
    >>> show_ref_map (ET_Trap,   "Ref_Req_Map")
    BMT.Trap
        ('BMT.Person_owns_Trap', ['right'])
        ('BMT.Person_sets_Trap_at_Location', ['middle'])
        ('BMT.Rodent_in_Trap', ['right'])

    >>> show_ref_map (ET_Person, "Ref_Opt_Map")
    >>> show_ref_map (ET_Trap,   "Ref_Opt_Map")

    >>> show_children (ET_Entity)
    MOM.Entity
      MOM.An_Entity
        MOM.Date_Interval
          MOM.Date_Interval_C
          MOM.Date_Interval_N
        MOM._Interval_
          MOM.Float_Interval
          MOM.Frequency_Interval
      MOM.Id_Entity
        MOM.Link
          MOM.Link1
            BMT.Rodent_is_sick
          MOM._MOM_Link_n_
            MOM.Link2
              MOM.Link2_Ordered
              BMT.Rodent_in_Trap
              BMT.Person_owns_Trap
            MOM.Link3
              BMT.Person_sets_Trap_at_Location
        MOM.Object
          MOM.Named_Object
            BMT.Rodent
              BMT.Mouse
                BMT.Beaver
                  BMT.Otter
              BMT.Rat
            BMT.Trap
              BMT.Supertrap
          BMT.Location
          BMT.Person

Scope
-----

A :class:`scope<_MOM.Scope.Scope>` manages the instances of essential
object and link types.

Specifying `None` as `db_url` will create an in memory database::

    >>> scope = MOM.Scope.new (apt, %(db_scheme)s)

For each :attr:`~_MOM.Entity.PNS` defining essential
classes, the `scope` provides an object holding
:class:`object managers<_MOM.E_Type_Manager.Object>` and
:class:`link managers<_MOM.E_Type_Manager.Link>`
that support instance creation and queries:

    .. ### DBW-specific start

    >>> scope.MOM.Id_Entity
    <E_Type_Manager for MOM.Id_Entity of scope BMT__Hash__HPS>
    >>> scope.BMT.Person
    <E_Type_Manager for BMT.Person of scope BMT__Hash__HPS>
    >>> scope.BMT.Person_owns_Trap
    <E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__HPS>

    .. ### DBW-specific finish

.. _`essential-primary-keys`:

Identity
--------

Essential objects and links have identity, i.e., each object or link
can be uniquely identified. This identity is specified by a set of (so
called `primary`) attributes that together define the
`essential primary key`, short `epk`, for the entity in question. If
there is more than one primary attribute, the sequence of the
attributes is defined by their :attr:`rank` and :attr:`name`.

Essential objects identified by a simple, unstructured `name` are
defined by classes derived from
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`. All other
essential objects are defined by classes derived from
:class:`MOM.Object<_MOM.Object.Object>` that specify one or more
essential attributes of kind :class:`~_MOM._Attr.Kind.Primary`.

Essential links are identified by the associated objects (the link's
roles) and any other, if any, primary attributes defined for the link
in question:

- Unary links are derived from :class:`MOM.Link1<_MOM.Link.Link1>`
  and identified by the link role :attr:`left<_MOM.Link.Link1.left>`
  plus any other primary attributes.

- Binary links are derived from :class:`MOM.Link2<_MOM.Link.Link2>`
  and identified by the link roles :attr:`left<_MOM.Link.Link2.left>`
  and :attr:`right<_MOM.Link.Link2.right>` plus any other primary
  attributes.

- Binary ordered links are derived from
  :class:`MOM.Link2_Ordered<_MOM.Link.Link2_Ordered>`
  and identified by the link roles
  :attr:`left<_MOM.Link.Link2_Ordered.left>`,
  :attr:`right<_MOM.Link.Link2_Ordered.right>`, and
  :attr:`seq_no<_MOM.Link.Link2_Ordered.seq_no>` plus any other primary
  attributes.

- Ternary links are derived from :class:`MOM.Link3<_MOM.Link.Link3>`
  and identified by the link roles :attr:`left<_MOM.Link.Link3.left>`,
  :attr:`middle<_MOM.Link.Link3.middle>`,
  and :attr:`right<_MOM.Link.Link3.right>` plus any other primary
  attributes.

Object and link creation
-------------------------

One creates objects or links by calling the etype manager of the
appropriate class:

    >>> scope.MOM.Named_Object ("foo")
    Traceback (most recent call last):
      ...
    Partial_Type: Named_Object

    >>> p     = scope.BMT.Person     ("luke", "lucky")
    >>> p
    BMT.Person (u'luke', u'lucky', u'')
    >>> q     = scope.BMT.Person     ("dog",  "snoopy")
    >>> l1    = scope.BMT.Location   (-16.268799, 48.189956)
    >>> l2    = scope.BMT.Location   (-16.740770, 48.463313)
    >>> m     = scope.BMT.Mouse      ("mighty_mouse")
    >>> b     = scope.BMT.Beaver     ("toothy_beaver")
    >>> r     = scope.BMT.Rat        ("rutty_rat")
    >>> axel  = scope.BMT.Rat        ("axel")
    >>> t1    = scope.BMT.Trap       ("x", 1)
    >>> t2    = scope.BMT.Trap       ("x", 2)
    >>> t3    = scope.BMT.Trap       ("y", 1)
    >>> t4    = scope.BMT.Trap       ("y", 2)
    >>> t5    = scope.BMT.Trap       ("z", 3)

    >>> Ris   = scope.BMT.Rodent_is_sick
    >>> RiT   = scope.BMT.Rodent_in_Trap
    >>> PoT   = scope.BMT.Person_owns_Trap
    >>> PTL   = scope.BMT.Person_sets_Trap_at_Location

    >>> m == m, m != m, m == b, m != b, m == "", m != ""
    (True, False, False, True, False, True)

    >>> RiT (p, t4)
    Traceback (most recent call last):
      ...
    ValueError: Person (u'luke', u'lucky', u'') not eligible for attribute left,
        must be instance of Rodent

    >>> rit1 = RiT (m, t1)
    >>> rit1
    BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1))
    >>> RiT (m, t2)
    Traceback (most recent call last):
      ...
    Multiplicity_Errors: Rodent_in_Trap, [Multiplicity(u"Maximum number of links for (u'mighty_mouse') is 1 ((BMT.Mouse (u'mighty_mouse'), BMT.Trap (u'x', 2)), [BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1))])",)]
    >>> RiT (r, t3)
    BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1))
    >>> RiT (axel, t2)
    BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2))

    >>> PoT (p, t1)
    BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1))
    >>> PoT (p, t2)
    BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2))
    >>> PoT (q, t3)
    BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1))
    >>> PoT (("tin", "tin"), t4)
    BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))

Creating a link will automatically set `auto_cached` attributes of the objects
participating of the link, like `Trap.setter` and `Trap.location`::

    >>> t1.setter, t1.location  ### before creation of Person_sets_Trap_at_Location
    (None, None)
    >>> PTL (p, t1, l1)
    BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956))
    >>> t1.setter, t1.location  ### after creation of Person_sets_Trap_at_Location
    (BMT.Person (u'luke', u'lucky', u''), BMT.Location (-16.268799, 48.189956))
    >>> t2.setter, t2.location  ### before creation of Person_sets_Trap_at_Location
    (None, None)
    >>> PTL (p, t2, l2)
    BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313))
    >>> t2.setter, t2.location  ### after creation of Person_sets_Trap_at_Location
    (BMT.Person (u'luke', u'lucky', u''), BMT.Location (-16.74077, 48.463313))
    >>> t3.setter, t3.location  ### before creation of Person_sets_Trap_at_Location
    (None, None)
    >>> PTL (p, t3, l2)
    BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))
    >>> t3.setter, t3.location  ### after creation of Person_sets_Trap_at_Location
    (BMT.Person (u'luke', u'lucky', u''), BMT.Location (-16.74077, 48.463313))

Queries
-------

One queries the object model by calling query methods of the
appropriate etype manager. Strict queries return only instances
of the essential class in question,
but not instances of derived classes. Non-strict queries are
transitive, i.e., they return instances of the essential class in
question and all its descendants. For partial types, strict queries
return nothing. By default, queries are non-strict (transitive).
Passing `strict = True` to a query makes it strict.

The query :meth:`instance<_MOM.E_Type_Manager.E_Type_Manager.instance>` can
only be applied to `E_Type_Managers` for essential types that are, or
inherit from, a `relevant_root`:

    >>> scope.MOM.Object.instance ("mighty_mouse")
    Traceback (most recent call last):
      ...
    TypeError: Object needs the arguments (), got (u'mighty_mouse',) instead
    >>> scope.MOM.Named_Object.instance ("mighty_mouse")
    BMT.Mouse (u'mighty_mouse')

    >>> scope.BMT.Rodent.instance ("mighty_mouse")
    BMT.Mouse (u'mighty_mouse')
    >>> print scope.BMT.Rat.instance ("mighty_mouse")
    None
    >>> print scope.BMT.Rat.query (name = "mighty_mouse").all ()
    []

    >>> PoT.query_s ().all ()
    [BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]
    >>> PoT.instance ((u'dog', u'snoopy'), (u'y', 1))
    BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1))
    >>> PoT.instance ((u'dog', u'snoopy', u''), (u'x', 2))
    >>> print PoT.instance (("Man", "tin"), t4)
    None

The query :meth:`exists<_MOM.E_Type_Manager.E_Type_Manager.exists>`
returns a list of all `E_Type_Managers` for which an object or link
with the specified `epk` exists:

    >>> scope.MOM.Named_Object.exists ("mighty_mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__HPS>]
    >>> scope.BMT.Mouse.exists ("mighty_mouse")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__HPS>]
    >>> scope.BMT.Rat.exists ("mighty_mouse")
    []

    >>> PoT.exists ((u'dog', u'snoopy'), (u'y', 1))
    [<E_Type_Manager for BMT.Person_owns_Trap of scope BMT__Hash__HPS>]
    >>> PoT.exists (("Man", "tin"), t4)
    []

The queries :attr:`~_MOM.E_Type_Manager.E_Type_Manager.count_strict`,
:attr:`~_MOM.E_Type_Manager.E_Type_Manager.count`,
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.query`, and
:meth:`~_MOM.E_Type_Manager.E_Type_Manager.r_query` return the
number, or list, of instances of the specified
etype:

    >>> scope.BMT.Mouse.count_strict
    1
    >>> list (scope.BMT.Mouse.query_s (strict = True))
    [BMT.Mouse (u'mighty_mouse')]
    >>> scope.BMT.Mouse.count
    2
    >>> list (scope.BMT.Mouse.query_s ())
    [BMT.Mouse (u'mighty_mouse'), BMT.Beaver (u'toothy_beaver')]

    >>> scope.BMT.Rat.count_strict
    2
    >>> list (scope.BMT.Rat.query_s (strict = True))
    [BMT.Rat (u'axel'), BMT.Rat (u'rutty_rat')]
    >>> scope.BMT.Rat.count
    2
    >>> list (scope.BMT.Rat.query_s ())
    [BMT.Rat (u'axel'), BMT.Rat (u'rutty_rat')]

    >>> scope.BMT.Rodent.count_strict
    0
    >>> list (scope.BMT.Rodent.query_s (strict = True))
    []
    >>> scope.BMT.Rodent.count
    4
    >>> list (scope.BMT.Rodent.query_s ())
    [BMT.Rat (u'axel'), BMT.Mouse (u'mighty_mouse'), BMT.Rat (u'rutty_rat'), BMT.Beaver (u'toothy_beaver')]

    >>> scope.MOM.Named_Object.count
    9
    >>> list (scope.MOM.Named_Object.query_s ())
    [BMT.Rat (u'axel'), BMT.Mouse (u'mighty_mouse'), BMT.Rat (u'rutty_rat'), BMT.Beaver (u'toothy_beaver'), BMT.Trap (u'x', 1), BMT.Trap (u'x', 2), BMT.Trap (u'y', 1), BMT.Trap (u'y', 2), BMT.Trap (u'z', 3)]
    >>> scope.MOM.Object.count
    14
    >>> list (scope.MOM.Object.query_s ())
    [BMT.Location (-16.74077, 48.463313), BMT.Location (-16.268799, 48.189956), BMT.Rat (u'axel'), BMT.Person (u'dog', u'snoopy', u''), BMT.Person (u'luke', u'lucky', u''), BMT.Mouse (u'mighty_mouse'), BMT.Rat (u'rutty_rat'), BMT.Person (u'tin', u'tin', u''), BMT.Beaver (u'toothy_beaver'), BMT.Trap (u'x', 1), BMT.Trap (u'x', 2), BMT.Trap (u'y', 1), BMT.Trap (u'y', 2), BMT.Trap (u'z', 3)]

    >>> list (scope.MOM.Id_Entity.query_s ())
    [BMT.Location (-16.74077, 48.463313), BMT.Location (-16.268799, 48.189956), BMT.Rat (u'axel'), BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2)), BMT.Person (u'dog', u'snoopy', u''), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person (u'luke', u'lucky', u''), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Mouse (u'mighty_mouse'), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1)), BMT.Rat (u'rutty_rat'), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person (u'tin', u'tin', u''), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2)), BMT.Beaver (u'toothy_beaver'), BMT.Trap (u'x', 1), BMT.Trap (u'x', 2), BMT.Trap (u'y', 1), BMT.Trap (u'y', 2), BMT.Trap (u'z', 3)]
    >>> scope.MOM.Id_Entity.count
    24

    >>> scope.MOM.Link.count
    10
    >>> list (scope.MOM.Link.query_s ())
    [BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    >>> scope.MOM.Link2.count
    7
    >>> list (scope.MOM.Link2.query_s ())
    [BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    >>> scope.MOM.Link3.count
    3
    >>> list (scope.MOM.Link3.query_s ())
    [BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]

    >>> sk_right_left = TFL.Sorted_By (RiT.right.sort_key, RiT.left.sort_key)
    >>> sk_right_left_pm = TFL.Sorted_By (RiT.right.sort_key_pm, RiT.left.sort_key_pm)
    >>> RiT.count
    3
    >>> show (RiT.query_s ())
    [((u'axel', ), (u'x', 2)), ((u'mighty_mouse', ), (u'x', 1)), ((u'rutty_rat', ), (u'y', 1))]
    >>> show (RiT.query_s (sort_key = sk_right_left))
    [((u'mighty_mouse', ), (u'x', 1)), ((u'axel', ), (u'x', 2)), ((u'rutty_rat', ), (u'y', 1))]

    >>> print formatted (sk_right_left (rit1)) #doctest: +NORMALIZE_WHITESPACE
    ( ( 'tuple'
      , ( ( 'unicode' , 'x' )
        , ( 'number' , 1 )
        )
      )
    , ( 'tuple'
      , ( ( 'unicode' , 'mighty_mouse' ) )
      )
    )
    >>> print formatted (sk_right_left_pm (rit1)) #doctest: +NORMALIZE_WHITESPACE
    ( ( 'tuple'
      , ( ( 'Type_Name_Type' , 'BMT.Trap' )
        , ( 'tuple'
          , ( ( 'unicode' , 'x' )
            , ( 'number' , 1 )
            )
          )
        )
      )
    , ( 'tuple'
      , ( ( 'Type_Name_Type' , 'BMT.Rodent' )
        , ( 'tuple'
          , ( ( 'unicode' , 'mighty_mouse' ) )
          )
        )
      )
    )

    >>> show (RiT.r_query_s (right = t1, strict = True))
    [((u'mighty_mouse', ), (u'x', 1))]
    >>> show (RiT.r_query_s (trap = ("x", 2)))
    [((u'axel', ), (u'x', 2))]
    >>> show (RiT.r_query_s (trap = ("y", "1"), strict = True))
    [((u'rutty_rat', ), (u'y', 1))]
    >>> show (RiT.r_query_s (right = m))
    []
    >>> show (RiT.r_query_s (left = "Foxy_Fox", strict = True))
    []

    >>> show (RiT.r_query_s (left = m))
    [((u'mighty_mouse', ), (u'x', 1))]
    >>> show (RiT.r_query_s (rodent = "rutty_rat"))
    [((u'rutty_rat', ), (u'y', 1))]
    >>> show (RiT.r_query_s (left = ("axel", ), strict = True))
    [((u'axel', ), (u'x', 2))]
    >>> show (RiT.r_query_s (left = "Jimmy", strict = True))
    []

    >>> PoT.count
    4
    >>> show (PoT.r_query_s (left = p))
    [((u'luke', u'lucky', u''), (u'x', 1)), ((u'luke', u'lucky', u''), (u'x', 2))]
    >>> show (PoT.r_query_s (person = ("dog",  "snoopy")))
    [((u'dog', u'snoopy', u''), (u'y', 1))]

    >>> PTL.count
    3
    >>> show (PTL.r_query_s (left = p, trap = t1))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (person = p, middle = ("x", 2)))
    [((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = ("luke", "lucky"), trap = t3, strict = True))
    [((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (left = q, middle = t1))
    []

    >>> show (PTL.r_query_s (left = p))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (location = (-16.74077, 48.463313)))
    [((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (trap = ("y", "1")))
    [((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = ("Tan", "Tan")))
    []

    >>> show (PTL.r_query_s (left = p))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (middle = (u'x', 2)))
    [((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (right = l1))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (trap = t2, location = l2))
    [((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (middle = (u'y', 1), right = l1))
    []
    >>> show (PTL.r_query_s (left = p, middle = (u'x', 2), right = l2))
    [((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313))]
    >>> show (PTL.r_query_s (person = p, trap = (u'x', 2), location = l1))
    []
    >>> show (PTL.r_query_s (person = p, trap = ('x', 1), location = l1))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956))]
    >>> show (PTL.r_query_s (left = ("Tan", "Tan")))
    []

    >>> show (PTL.links_of (p))
    [((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]

    >>> t1
    BMT.Trap (u'x', 1)
    >>> t1.all_links ()
    [BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1))]

    >>> list (scope)
    [BMT.Location (-16.268799, 48.189956), BMT.Location (-16.74077, 48.463313), BMT.Person (u'luke', u'lucky', u''), BMT.Person (u'dog', u'snoopy', u''), BMT.Person (u'tin', u'tin', u''), BMT.Mouse (u'mighty_mouse'), BMT.Beaver (u'toothy_beaver'), BMT.Rat (u'rutty_rat'), BMT.Rat (u'axel'), BMT.Trap (u'x', 1), BMT.Trap (u'x', 2), BMT.Trap (u'y', 1), BMT.Trap (u'y', 2), BMT.Trap (u'z', 3), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313))]

    >>> len (list (scope))
    24

Changing objects and links
---------------------------

    >>> old_id = axel.pid
    >>> axel.all_links ()
    [BMT.Rodent_in_Trap ((u'axel', ), (u'x', 2))]
    >>> axel.name = "betty"
    Traceback (most recent call last):
      ...
    AttributeError: Primary attribute `Rat.name` cannot be assigned.
    Use `set` or `set_raw` to change it.
    >>> axel.set (name = "betty")
    1
    >>> axel
    BMT.Rat (u'betty')
    >>> axel.pid == old_id
    True
    >>> axel.all_links ()
    [BMT.Rodent_in_Trap ((u'betty', ), (u'x', 2))]

    >>> print p.as_code ()
    BMT.Person (u'luke', u'lucky', u'', )
    >>> p.set (middle_name = "zacharias")
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_middle_name_length` : Value for middle_name must not be longer than 5 (length <= 5)
        length = 9 << len (middle_name)
        middle_name = 'zacharias'

    >>> m
    BMT.Mouse (u'mighty_mouse')
    >>> m.color, m.weight
    (u'', None)
    >>> print m.as_code ()
    BMT.Mouse (u'mighty_mouse', )
    >>> m.color = "white"
    >>> print m.as_code ()
    BMT.Mouse (u'mighty_mouse', color = u'white')
    >>> m.weight = 0
    Traceback (most recent call last):
      ...
    Invariant: Condition `AC_check_weight_0` : weight > 0
        weight = 0.0
    >>> m.set (weight = -5.0)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_weight_0` : weight > 0
        weight = -5.0
    >>> m.weight = 10
    >>> print m.as_code ()
    BMT.Mouse (u'mighty_mouse', color = u'white', weight = 10.0)
    >>> m.set (color = "black", weight = 25.0)
    2
    >>> print m.as_code ()
    BMT.Mouse (u'mighty_mouse', color = u'black', weight = 25.0)
    >>> try :
    ...   m.set (weight = "'one ton'")
    ... except ValueError :
    ...   pass
    Error in `cooked` of `Float `weight`` for value `'one ton'` [(u'mighty_mouse')]
    >>> m.set_raw (weight = "one ton")
    Traceback (most recent call last):
      ...
    Attribute_Value: Can't set necessary attribute Mouse.weight to `u'one ton'`
        `Syntax error` for : `Float `weight``
         expected type  : `Float`
         got      value : `one ton`
    >>> m.set_raw (color = "yellow", weight = "6*7")
    2
    >>> m.color, m.weight
    (u'yellow', 42.0)
    >>> print m.as_code ()
    BMT.Mouse (u'mighty_mouse', color = u'yellow', weight = 42.0)

    >>> csk = TFL.Sorted_By (Q.parent != None, Q.cid)
    >>> for c in m.changes ().order_by (csk).all () : ### ???
    ...     print c
    <Create BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), new-values = {'last_cid' : '5'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'', 'last_cid' : '5'}, new-values = {'color' : u'white', 'last_cid' : '26'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'last_cid' : '26', 'weight' : u''}, new-values = {'last_cid' : '27', 'weight' : u'10.0'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'white', 'last_cid' : '27', 'weight' : u'10.0'}, new-values = {'color' : u'black', 'last_cid' : '28', 'weight' : u'25.0'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'black', 'last_cid' : '28', 'weight' : u'25.0'}, new-values = {'color' : u'yellow', 'last_cid' : '29', 'weight' : u'42.0'}>

    >>> mm = m.copy ("Magic_Mouse")
    >>> for c in mm.changes ().order_by (csk).all () :
    ...     print c
    <Copy BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), new-values = {'last_cid' : '32'}>
        <Create BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), new-values = {'last_cid' : '30'}>
        <Modify BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), old-values = {'color' : u'', 'last_cid' : '30', 'weight' : u''}, new-values = {'color' : u'yellow', 'last_cid' : '31', 'weight' : u'42.0'}>
    <Create BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), new-values = {'last_cid' : '30'}>
    <Modify BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), old-values = {'color' : u'', 'last_cid' : '30', 'weight' : u''}, new-values = {'color' : u'yellow', 'last_cid' : '31', 'weight' : u'42.0'}>

    >>> print l1.as_code ()
    BMT.Location (-16.268799, 48.189956, )
    >>> l1.set (lat =  91.5)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_lat_1` : -90.0 <= lat <= 90.0
        lat = 91.5
    >>> l1.set (lon = 270.0)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_lon_1` : -180.0 <= lon <= 180.0
        lon = 270.0
    >>> print l1.as_code ()
    BMT.Location (-16.268799, 48.189956, )

    >>> rit = RiT.instance (m, t1)
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1), )
    >>> print rit.rodent.as_code ()
    BMT.Mouse (u'mighty_mouse', color = u'yellow', weight = 42.0)
    >>> print rit.trap.as_code ()
    BMT.Trap (u'x', 1, )
    >>> print rit.is_g_correct ()
    True
    >>> rit.trap.max_weight = 20
    >>> print rit.is_g_correct ()
    False
    >>> for err in rit.errors :
    ...     print err
    Condition `valid_weight` : Weight of `rodent` must not exceed `max_weight` of `trap`. (rodent.weight <= trap.max_weight)
        rodent = mighty_mouse
        rodent.weight = 42.0
        trap = x, 1
        trap.max_weight = 20.0

    >>> pot = PoT.instance (p, t1)
    >>> pot.price = float ("1.20")
    >>> print pot.as_code ()
    BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1), price = 1.2)

    >>> lcp = scope.query_changes (type_name = "BMT.Person").order_by (TFL.Sorted_By ("-cid")).first ()
    >>> lcp.cid, lcp.epk
    (20, (u'tin', u'tin', u'', 'BMT.Person'))
    >>> lcp
    <Create BMT.Person (u'tin', u'tin', u'', 'BMT.Person'), new-values = {'last_cid' : '20'}>

    >>> lct = scope.query_changes (type_name = "BMT.Trap").order_by (TFL.Sorted_By ("-cid")).first ()
    >>> lct.cid, lct.epk
    (33, (u'x', u'1', 'BMT.Trap'))
    >>> lct
    <Modify BMT.Trap (u'x', u'1', 'BMT.Trap'), old-values = {'last_cid' : '9', 'max_weight' : u''}, new-values = {'last_cid' : '33', 'max_weight' : u'20.0'}>

Attribute queries
------------------

    >>> scope.BMT.Person.query_s (Q.last_name == Q.first_name).all ()
    [BMT.Person (u'tin', u'tin', u'')]
    >>> scope.BMT.Rodent.query_s (Q.weight != None).all ()
    [BMT.Mouse (u'Magic_Mouse'), BMT.Mouse (u'mighty_mouse')]
    >>> scope.BMT.Rodent.query_s (Q.weight == None).all ()
    [BMT.Rat (u'betty'), BMT.Rat (u'rutty_rat'), BMT.Beaver (u'toothy_beaver')]
    >>> scope.BMT.Rodent.query_s (Q.weight > 0).all ()
    [BMT.Mouse (u'Magic_Mouse'), BMT.Mouse (u'mighty_mouse')]
    >>> scope.BMT.Trap.query_s (Q.serial_no > 1).all ()
    [BMT.Trap (u'x', 2), BMT.Trap (u'y', 2), BMT.Trap (u'z', 3)]
    >>> scope.BMT.Trap.query_s (Q.serial_no < 2).all ()
    [BMT.Trap (u'x', 1), BMT.Trap (u'y', 1)]
    >>> scope.BMT.Trap.query_s (Q.serial_no %% 2).all ()
    [BMT.Trap (u'x', 1), BMT.Trap (u'y', 1), BMT.Trap (u'z', 3)]
    >>> scope.BMT.Trap.query_s (Q.serial_no %% 2 == 0).all ()
    [BMT.Trap (u'x', 2), BMT.Trap (u'y', 2)]

    >>> tuple (scope.BMT.Rodent.query_s (Q.weight != None).attr (Q.weight))
    (42.0, 42.0)
    >>> tuple (scope.BMT.Rodent.query_s (Q.weight == None).attrs (Q.name, "color"))
    ((u'betty', u''), (u'rutty_rat', u''), (u'toothy_beaver', u''))
    >>> tuple (scope.BMT.Trap.query_s (Q.serial_no %% 2).attr (Q.up_ex_q))
    (20.0, None, None)

Renaming objects and links
--------------------------

    >>> b.all_links ()
    []
    >>> rit.set (left = b)
    1
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'toothy_beaver', ), (u'x', 1), )
    >>> b.all_links ()
    [BMT.Rodent_in_Trap ((u'toothy_beaver', ), (u'x', 1))]
    >>> rit.rodent, rit.right
    (BMT.Beaver (u'toothy_beaver'), BMT.Trap (u'x', 1))

    >>> rit.set (rodent = m)
    1
    >>> print rit.as_code ()
    BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1), )

Deleting objects and links
--------------------------

    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Rodent_in_Trap ((u'betty', ), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'mighty_mouse', ), (u'x', 1)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    .. ### DBW-specific start

    >>> m.object_referring_attributes
    defaultdict(<type 'list'>, {})
    >>> print formatted1 (sorted (d.type_name for d in m.dependencies))
    ['BMT.Rodent_in_Trap']
    >>> print formatted1 (sorted (d.type_name for d in t1.dependencies)) ### 1
    ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location', 'BMT.Rodent_in_Trap']

    >>> m_id  = m.pid
    >>> t1_id = t1.pid
    >>> t2_id = t2.pid
    >>> show (scope.ems.all_links (m_id))
    [((u'mighty_mouse', ), (u'x', 1))]

    .. ### DBW-specific finish

    >>> show (t1.all_links ())
    [((u'luke', u'lucky', u''), (u'x', 1)), ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), ((u'mighty_mouse', ), (u'x', 1))]

    >>> t1.catch
    BMT.Mouse (u'mighty_mouse')
    >>> m
    BMT.Mouse (u'mighty_mouse')
    >>> m.destroy ()
    >>> t1.catch

    >>> show (t1.all_links ())
    [((u'luke', u'lucky', u''), (u'x', 1)), ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956))]

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (m_id))
    []

    >>> print formatted1 (sorted (d.type_name for d in t1.dependencies)) ### 2
    ['BMT.Person_owns_Trap', 'BMT.Person_sets_Trap_at_Location']

    .. ### DBW-specific finish

    >>> scope.MOM.Link.query_s ().count ()
    9
    >>> scope.MOM.Link.r_query_s ().all ()
    [BMT.Rodent_in_Trap ((u'betty', ), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 1), (-16.268799, 48.189956)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    >>> t1.destroy ()

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (t1_id))
    []
    >>> show (scope.ems.all_links (t2_id))
    [((u'luke', u'lucky', u''), (u'x', 2)), ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), ((u'betty', ), (u'x', 2))]

    .. ### DBW-specific finish

    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Rodent_in_Trap ((u'betty', ), (u'x', 2)), BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_owns_Trap ((u'luke', u'lucky', u''), (u'x', 2)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'x', 2), (-16.74077, 48.463313)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    >>> t2.destroy ()
    >>> scope.MOM.Link.query_s ().all ()
    [BMT.Person_owns_Trap ((u'dog', u'snoopy', u''), (u'y', 1)), BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u''), (u'y', 1), (-16.74077, 48.463313)), BMT.Rodent_in_Trap ((u'rutty_rat', ), (u'y', 1)), BMT.Person_owns_Trap ((u'tin', u'tin', u''), (u'y', 2))]

    .. ### DBW-specific start

    >>> show (scope.ems.all_links (t2_id))
    []

    .. ### DBW-specific finish

Scope queries
--------------

    >>> for e in scope.i_incorrect () :
    ...     print list (e.errors)

    >>> for e in scope.g_incorrect () :
    ...     print list (str (x).replace (NL, " ") for x in e.errors)
    [u'Condition `completely_defined` : All necessary attributes must be defined. Necessary attribute Float `weight` is not defined']
    [u'Condition `completely_defined` : All necessary attributes must be defined. Necessary attribute Float `weight` is not defined']
    [u'Condition `completely_defined` : All necessary attributes must be defined. Necessary attribute Float `weight` is not defined']

    >>> len (scope.uncommitted_changes)
    37
    >>> for c in scope.uncommitted_changes :
    ...     print c
    <Create BMT.Person (u'luke', u'lucky', u'', 'BMT.Person'), new-values = {'last_cid' : '1'}>
    <Create BMT.Person (u'dog', u'snoopy', u'', 'BMT.Person'), new-values = {'last_cid' : '2'}>
    <Create BMT.Location (u'-16.268799', u'48.189956', 'BMT.Location'), new-values = {'last_cid' : '3'}>
    <Create BMT.Location (u'-16.74077', u'48.463313', 'BMT.Location'), new-values = {'last_cid' : '4'}>
    <Create BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), new-values = {'last_cid' : '5'}>
    <Create BMT.Beaver (u'toothy_beaver', 'BMT.Beaver'), new-values = {'last_cid' : '6'}>
    <Create BMT.Rat (u'rutty_rat', 'BMT.Rat'), new-values = {'last_cid' : '7'}>
    <Create BMT.Rat (u'axel', 'BMT.Rat'), new-values = {'last_cid' : '8'}>
    <Create BMT.Trap (u'x', u'1', 'BMT.Trap'), new-values = {'last_cid' : '9'}>
    <Create BMT.Trap (u'x', u'2', 'BMT.Trap'), new-values = {'last_cid' : '10'}>
    <Create BMT.Trap (u'y', u'1', 'BMT.Trap'), new-values = {'last_cid' : '11'}>
    <Create BMT.Trap (u'y', u'2', 'BMT.Trap'), new-values = {'last_cid' : '12'}>
    <Create BMT.Trap (u'z', u'3', 'BMT.Trap'), new-values = {'last_cid' : '13'}>
    <Create BMT.Rodent_in_Trap ((u'mighty_mouse', 'BMT.Mouse'), (u'x', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), new-values = {'last_cid' : '14'}>
    <Create BMT.Rodent_in_Trap ((u'rutty_rat', 'BMT.Rat'), (u'y', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), new-values = {'last_cid' : '15'}>
    <Create BMT.Rodent_in_Trap ((u'axel', 'BMT.Rat'), (u'x', u'2', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), new-values = {'last_cid' : '16'}>
    <Create BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), new-values = {'last_cid' : '17'}>
    <Create BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'2', 'BMT.Trap'), 'BMT.Person_owns_Trap'), new-values = {'last_cid' : '18'}>
    <Create BMT.Person_owns_Trap ((u'dog', u'snoopy', u'', 'BMT.Person'), (u'y', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), new-values = {'last_cid' : '19'}>
    <Create BMT.Person (u'tin', u'tin', u'', 'BMT.Person'), new-values = {'last_cid' : '20'}>
    <Create BMT.Person_owns_Trap ((u'tin', u'tin', u'', 'BMT.Person'), (u'y', u'2', 'BMT.Trap'), 'BMT.Person_owns_Trap'), new-values = {'last_cid' : '21'}>
    <Create BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), (u'-16.268799', u'48.189956', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), new-values = {'last_cid' : '22'}>
    <Create BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'2', 'BMT.Trap'), (u'-16.74077', u'48.463313', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), new-values = {'last_cid' : '23'}>
    <Create BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'y', u'1', 'BMT.Trap'), (u'-16.74077', u'48.463313', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), new-values = {'last_cid' : '24'}>
    <Modify BMT.Rat (u'betty', 'BMT.Rat'), old-values = {'last_cid' : '8', 'name' : u'axel'}, new-values = {'last_cid' : '25', 'name' : u'betty'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'', 'last_cid' : '5'}, new-values = {'color' : u'white', 'last_cid' : '26'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'last_cid' : '26', 'weight' : u''}, new-values = {'last_cid' : '27', 'weight' : u'10.0'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'white', 'last_cid' : '27', 'weight' : u'10.0'}, new-values = {'color' : u'black', 'last_cid' : '28', 'weight' : u'25.0'}>
    <Modify BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'black', 'last_cid' : '28', 'weight' : u'25.0'}, new-values = {'color' : u'yellow', 'last_cid' : '29', 'weight' : u'42.0'}>
    <Copy BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), new-values = {'last_cid' : '32'}>
        <Create BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), new-values = {'last_cid' : '30'}>
        <Modify BMT.Mouse (u'Magic_Mouse', 'BMT.Mouse'), old-values = {'color' : u'', 'last_cid' : '30', 'weight' : u''}, new-values = {'color' : u'yellow', 'last_cid' : '31', 'weight' : u'42.0'}>
    <Modify BMT.Trap (u'x', u'1', 'BMT.Trap'), old-values = {'last_cid' : '9', 'max_weight' : u''}, new-values = {'last_cid' : '33', 'max_weight' : u'20.0'}>
    <Modify BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), old-values = {'last_cid' : '17', 'price' : u'42.0'}, new-values = {'last_cid' : '34', 'price' : u'1.2'}>
    <Modify BMT.Rodent_in_Trap ((u'toothy_beaver', 'BMT.Beaver'), (u'x', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), old-values = {'last_cid' : '14', 'left' : 5}, new-values = {'last_cid' : '35', 'left' : 6}>
    <Modify BMT.Rodent_in_Trap ((u'mighty_mouse', 'BMT.Mouse'), (u'x', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), old-values = {'last_cid' : '35', 'left' : 6}, new-values = {'last_cid' : '36', 'left' : 5}>
    <Destroy BMT.Mouse (u'mighty_mouse', 'BMT.Mouse'), old-values = {'color' : u'yellow', 'last_cid' : '29', 'weight' : u'42.0'}>
        <Destroy BMT.Rodent_in_Trap ((u'mighty_mouse', 'BMT.Mouse'), (u'x', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), old-values = {'last_cid' : '36'}>
    <Destroy BMT.Trap (u'x', u'1', 'BMT.Trap'), old-values = {'last_cid' : '33', 'max_weight' : u'20.0'}>
        <Destroy BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), old-values = {'last_cid' : '34', 'price' : u'1.2'}>
        <Destroy BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), (u'-16.268799', u'48.189956', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), old-values = {'last_cid' : '22'}>
    <Destroy BMT.Trap (u'x', u'2', 'BMT.Trap'), old-values = {'last_cid' : '10'}>
        <Destroy BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'2', 'BMT.Trap'), 'BMT.Person_owns_Trap'), old-values = {'last_cid' : '18'}>
        <Destroy BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'2', 'BMT.Trap'), (u'-16.74077', u'48.463313', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), old-values = {'last_cid' : '23'}>
        <Destroy BMT.Rodent_in_Trap ((u'betty', 'BMT.Rat'), (u'x', u'2', 'BMT.Trap'), 'BMT.Rodent_in_Trap'), old-values = {'last_cid' : '16'}>
    >>> c = scope.uncommitted_changes [-2]
    >>> pckl = c.as_pickle (True)
    >>> cc = c.from_pickle (pckl)
    >>> cc
    <Destroy BMT.Trap (u'x', u'1', 'BMT.Trap'), old-values = {'last_cid' : '33', 'max_weight' : u'20.0'}>
        <Destroy BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), old-values = {'last_cid' : '34', 'price' : u'1.2'}>
        <Destroy BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), (u'-16.268799', u'48.189956', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), old-values = {'last_cid' : '22'}>
    >>> cc.children
    [<Destroy BMT.Person_owns_Trap ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap'), old-values = {'last_cid' : '34', 'price' : u'1.2'}>, <Destroy BMT.Person_sets_Trap_at_Location ((u'luke', u'lucky', u'', 'BMT.Person'), (u'x', u'1', 'BMT.Trap'), (u'-16.268799', u'48.189956', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location'), old-values = {'last_cid' : '22'}>]
    >>> cc.children [0].parent is cc
    True
    >>> pckl = c.as_pickle ()
    >>> cc = c.from_pickle (pckl)
    >>> cc
    <Destroy BMT.Trap (u'x', u'1', 'BMT.Trap'), old-values = {'last_cid' : '33', 'max_weight' : u'20.0'}>
    >>> cc.children
    []
    >>> scope.commit ()
    >>> len (scope.uncommitted_changes)
    0

Replaying changes
-----------------

    >>> scop2 = MOM.Scope.new (apt, %(db_scheme)s)
    >>> tuple (s.MOM.Id_Entity.count for s in (scope, scop2))
    (16, 0)
    >>> for c in scope.query_changes (Q.parent == None).order_by (Q.cid) :
    ...     c.redo (scop2)
    >>> tuple (s.MOM.Id_Entity.count for s in (scope, scop2))
    (16, 16)
    >>> sorted (scope.user_diff (scop2, ignore = ["last_cid"]).iteritems ())
    []

    >>> t3.max_weight = 25
    >>> sorted (scope.user_diff (scop2, ignore = ["last_cid"]).iteritems ())
    [(('BMT.Trap', (u'y', u'1', 'BMT.Trap')), {'max_weight': ((25.0,), u'<Missing>')})]
    >>> scop2.BMT.Trap.instance (* t3.epk_raw, raw = True).set (max_weight = 42)
    1
    >>> sorted (scope.user_diff (scop2, ignore = ["last_cid"]).iteritems ())
    [(('BMT.Trap', (u'y', u'1', 'BMT.Trap')), {'max_weight': ((25.0,), (42.0,))})]
    >>> t3.destroy ()
    >>> for diff in sorted (scop2.user_diff (scope, ignore = ["last_cid"]).iteritems ()) :
    ...     print diff
    (('BMT.Person_owns_Trap', ((u'dog', u'snoopy', u'', 'BMT.Person'), (u'y', u'1', 'BMT.Trap'), 'BMT.Person_owns_Trap')), u'Present in Scope <hps://>, missing in Scope <hps://>')
    (('BMT.Person_sets_Trap_at_Location', ((u'luke', u'lucky', u'', 'BMT.Person'), (u'y', u'1', 'BMT.Trap'), (u'-16.74077', u'48.463313', 'BMT.Location'), 'BMT.Person_sets_Trap_at_Location')), u'Present in Scope <hps://>, missing in Scope <hps://>')
    (('BMT.Rodent_in_Trap', ((u'rutty_rat', 'BMT.Rat'), (u'y', u'1', 'BMT.Trap'), 'BMT.Rodent_in_Trap')), u'Present in Scope <hps://>, missing in Scope <hps://>')
    (('BMT.Trap', (u'y', u'1', 'BMT.Trap')), u'Present in Scope <hps://>, missing in Scope <hps://>')
    >>> scope.user_equal (scop2)
    False

Saving and re-loading changes from a database
----------------------------------------------

    >>> db_path   = %(db_path)s
    >>> db_url    = "/".join ((%(db_scheme)s, %(db_path)s))
    >>> db_path_x = db_path + ".x"
    >>> if sos.path.exists (db_path) :
    ...     sos.remove (db_path)
    >>> if sos.path.exists (db_path_x) :
    ...     sos.rmdir (db_path_x, deletefiles = True)

    >>> scope.MOM.Id_Entity.count
    12
    >>> scop3 = scope.copy (apt, db_url)
    >>> tuple (s.MOM.Id_Entity.count for s in (scope, scop3))
    (12, 12)
    >>> sorted (scop3.user_diff (scope).iteritems ())
    []
    >>> all ((s.pid, s.as_pickle_cargo ()) == (t.pid, t.as_pickle_cargo ()) for (s, t) in zip (scope, scop3))
    True
    >>> scop3.destroy ()

    >>> scop4 = MOM.Scope.load (apt, db_url)
    >>> tuple (s.MOM.Id_Entity.count for s in (scope, scop4))
    (12, 12)
    >>> sorted (scope.user_diff (scop4).iteritems ())
    []
    >>> all ((s.pid, s.as_pickle_cargo ()) == (t.pid, t.as_pickle_cargo ()) for (s, t) in zip (scope, scop4))
    True
    >>> scop4.destroy ()

    >>> if sos.path.exists (db_path) : sos.remove (db_path)

Migrating all entities and the complete change history
------------------------------------------------------

    >>> scope.MOM.Id_Entity.count
    12
    >>> scope.query_changes ().count ()
    50
    >>> scop5 = scope.copy (apt, %(db_scheme)s)
    >>> tuple (s.MOM.Id_Entity.count for s in (scope, scop5))
    (12, 12)
    >>> tuple (s.query_changes ().count () for s in (scope, scop5))
    (50, 50)
    >>> all ((s.pid, s.as_pickle_cargo ()) == (t.pid, t.as_pickle_cargo ()) for (s, t) in zip (scope, scop5))
    True
    >>> all ((s.cid, s.pid) == (t.cid, t.pid) for (s, t) in zip (* (s.query_changes () for s in (scope, scop5))))
    True
    >>> scop5.destroy ()

Primary key attributes
-----------------------

    >>> scope.BMT.Trap ("", None)
    Traceback (most recent call last):
    ...
    Invariants: Condition `name_not_empty` : name is not None and name != ''
        name = ''
      Condition `serial_no_not_empty` : serial_no is not None and serial_no != ''
        serial_no = None
    >>> scope.BMT.Trap ("ha", None)
    Traceback (most recent call last):
    ...
    Invariants: Condition `serial_no_not_empty` : serial_no is not None and serial_no != ''
        serial_no = None
    >>> scope.BMT.Trap ("", 0)
    Traceback (most recent call last):
    ...
    Invariants: Condition `name_not_empty` : name is not None and name != ''
        name = ''
    >>> scope.BMT.Trap (None, 0)
    Traceback (most recent call last):
    ...
    Invariants: Condition `name_not_empty` : name is not None and name != ''
        name = None
    >>> scope.BMT.Trap ("ha", "", raw = True)
    Traceback (most recent call last):
    ...
    Invariants: Condition `serial_no_not_empty` : serial_no is not None and serial_no != ''
        serial_no = None
    >>> scope.BMT.Trap ("", "7", raw = True)
    Traceback (most recent call last):
    ...
    Invariants: Condition `name_not_empty` : name is not None and name != ''
        name = ''

Rollback of uncommited changes
------------------------------

    >>> scope.changes_to_save
    2
    >>> scope.commit ()
    >>> scope.changes_to_save, scope.ems.max_cid ### before rollback
    (0, 50)
    >>> rbm = scope.BMT.Mouse ("Rollback_Mouse_1")
    >>> rbt = scope.BMT.Trap  ("Rollback_Trap_1", 1)
    >>> rbl = scope.BMT.Rodent_in_Trap (rbm, rbt)
    >>> scope.changes_to_save, scope.ems.max_cid
    (3, 53)
    >>> scope.BMT.Rodent.exists ("Rollback_Mouse_1")
    [<E_Type_Manager for BMT.Mouse of scope BMT__Hash__HPS>]
    >>> scope.rollback ()
    >>> scope.changes_to_save, scope.ems.max_cid ### after rollback
    (0, 50)
    >>> scope.BMT.Rodent.exists ("Rollback_Mouse_1")
    []

Auto-updating attributes
-------------------------

An attribute can be updated automatically whenever the value of
another attribute changes. To define an auto-updating attribute,
specify the (names of the) attributes it depends on in
`auto_up_depends`.

    >>> t4.max_weight = 10
    >>> t4.max_weight, t4.serial_no
    (10.0, 2)
    >>> t4.up_ex, t4.up_ex_q
    (20.0, 20.0)
    >>> t4.max_weight = 5
    >>> t4.up_ex
    10.0
    >>> del t4.max_weight
    >>> t4.up_ex, t4.up_ex_q
    (None, None)

Unary links
-----------

    >>> sr = scope.BMT.Mouse ("Sick_Rodent")
    >>> osm = Ris (sr, scope.MOM.Date_Interval (start = "20100218", raw = True))
    >>> osm.as_code ()
    u"BMT.Rodent_is_sick ((u'Sick_Rodent', ), dict (start = u'2010/02/18'), )"
    >>> osm.fever = 42
    >>> osm.as_code ()
    u"BMT.Rodent_is_sick ((u'Sick_Rodent', ), dict (start = u'2010/02/18'), fever = 42.0)"
    >>> sorted (sr.sickness)
    [BMT.Rodent_is_sick ((u'Sick_Rodent', ), dict (start = u'2010/02/18'))]

Changing a composite primary attribute
--------------------------------------

    >>> old_epk = osm.epk
    >>> old_epk
    (BMT.Mouse (u'Sick_Rodent'), MOM.Date_Interval (start = 2010/02/18), 'BMT.Rodent_is_sick')
    >>> Ris.instance (* old_epk)
    BMT.Rodent_is_sick ((u'Sick_Rodent', ), dict (start = u'2010/02/18'))

    .. ### DBW-specific start

    >>> sorted (scope.ems._tables [osm.relevant_root.type_name])
    [(26, (datetime.date(2010, 2, 18), None))]

    .. ### DBW-specific finish

    >>> osm.sick_leave.set_raw (start = "2010/03/01")
    1
    >>> print Ris.instance (* old_epk)
    None
    >>> osm.epk
    (BMT.Mouse (u'Sick_Rodent'), MOM.Date_Interval (start = 2010/03/01), 'BMT.Rodent_is_sick')
    >>> Ris.instance (* osm.epk)
    BMT.Rodent_is_sick ((u'Sick_Rodent', ), dict (start = u'2010/03/01'))

    .. ### DBW-specific start

    >>> sorted (scope.ems._tables [osm.relevant_root.type_name])
    [(26, (datetime.date(2010, 3, 1), None))]

    .. ### DBW-specific finish

Setting attribute values with Queries
-------------------------------------

    >>> tuple (scope.BMT.Trap.query_s (Q.serial_no != None).attrs (Q.serial_no, Q.max_weight, Q.up_ex_q))
    ((2, None, None), (3, None, None))
    >>> scope.BMT.Trap.query_s (Q.serial_no != None).set (max_weight = 25)
    >>> tuple (scope.BMT.Trap.query_s (Q.serial_no != None).attrs (Q.serial_no, Q.max_weight, Q.up_ex_q))
    ((2, 25.0, 50.0), (3, 25.0, 75.0))

"""

from   _TFL.Formatter           import Formatter, formatted_1 as formatted1
formatted  = Formatter (width = 240)

from   _MOM.inspect             import show_ref_map, show_ref_maps

__doc__ = doctest = dt_form % dict \
    ( import_DBW = "from _MOM._DBW._HPS.Manager import Manager"
    , import_EMS = "from _MOM._EMS.Hash         import Manager"
    , db_path    = "'/tmp/bmt_test.bmt'"
    , db_scheme  = "'hps://'"
    )
### __END__ GTW.__test__.MOM