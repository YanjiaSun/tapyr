# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.Attr.Kind
#
# Purpose
#    Provide descriptor classes for various attribute kinds of MOM
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Kind)
#    28-Sep-2009 (CT) Creation continued
#    29-Sep-2009 (CT) Creation continued..
#     6-Oct-2009 (CT) Creation continued...: `Primary`: method redefinitions
#     7-Oct-2009 (CT) Creation continued....: `set_cooked` folded into `__set__`
#     9-Oct-2009 (CT) `_symbolic_default` and `raw_default` added
#     9-Oct-2009 (CT) `Primary.__set__` changed to raise unconditionally
#     9-Oct-2009 (CT) `Sticky_Mixin` changed to use `reset` instead of
#                     homegrown code
#    12-Oct-2009 (CT) `is_primary` and `is_settable` added
#    19-Oct-2009 (CT) `changed = 42` added to various `set`-specific methods
#                     to avoid change checks during `reset`
#    20-Oct-2009 (MH) `s/TOM/MOM/g`
#    21-Oct-2009 (CT) `Class_Uses_Default_Mixin` removed
#    22-Oct-2009 (CT) Use `M_Attr_Kind` as meta
#    22-Oct-2009 (CT) s/default/raw_default/ where necessary
#    22-Oct-2009 (CT) `_Raw_Value_Mixin_` factored
#    28-Oct-2009 (CT) I18N
#    29-Oct-2009 (CT) `rank` added
#    ��revision-date�����
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

import _TFL._Meta.Property

import _MOM._Attr
import _MOM._Meta.M_Attr_Kind
import _MOM._Prop.Kind

from   _TFL.I18N             import _, _T, _Tn

class Kind (MOM.Prop.Kind) :
    """Root class of attribute kinds to be used as properties for essential
       attributes of the MOM meta object model.
    """

    __metaclass__         = MOM.Meta.M_Attr_Kind

    attr                  = None
    is_primary            = False
    is_settable           = True
    needs_raw_value       = False
    prop                  = TFL.Meta.Alias_Property ("attr")
    sync                  = None
    Table                 = dict ()

    def __init__ (self, Attr_Type) :
        attr = Attr_Type      (self)
        self.__super.__init__ (attr)
        self._check_sanity    (attr)
        self.rank           = (attr._t_rank, attr.rank)
        self.record_changes = attr.record_changes and self.record_changes
    # end def __init__

    def __delete__ (self, obj) :
        self.reset (obj)
    # end def __delete__

    def __get__ (self, obj, cls) :
        if obj is None :
            return self
        return self.get_value (obj)
    # end def __get__

    def __set__ (self, obj, value) :
        self.attr.check_invariant (obj, value)
        if self.record_changes and self.get_value (obj) != value :
            obj.home_scope.record_change \
                ( MOM.SCM.Entity_Change_Attr
                , obj, {self.name : self.get_raw (obj)}
                )
        self._set_cooked (obj, value)
    # end def __set__

    def get_raw (self, obj) :
        val = self.get_value (obj)
        if val is not None :
            return self.attr.as_string (val) or ""
        else :
            return ""
    # end def get_raw

    def get_value (self, obj) :
        return getattr (obj, self.attr.ckd_name, None)
    # end def get_value

    def inc_changes (self, man, obj, value) :
        ### don't redefine this (redefine `_inc_changes` instead)
        ### (this allows applications to extend `inc_changes` without having
        ### to know all classes redefining `_inc_changes`) !!!
        return self._inc_changes (man, obj, value)
    # end def inc_changes

    def reset (self, obj) :
        if self.attr._symbolic_default :
            self.set_raw \
                (obj, self.attr.raw_default, dont_raise = True, changed = True)
        else :
            if self.attr.raw_default and self.attr.default is None :
                self.attr.default = self.attr.from_string \
                    (self.attr.raw_default, obj, obj.globals ())
            self._set_raw \
                (obj, self.attr.raw_default, self.attr.default, changed = True)
    # end def reset

    def set_raw (self, obj, raw_value, glob_dict = None, dont_raise = False, changed = 42) :
        if glob_dict is None :
            glob_dict = obj.globals ()
        value = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, glob_dict)
                self.attr.check_invariant     (obj, value)
            except StandardError, exc :
                if dont_raise :
                    if __debug__ :
                        print exc
                else :
                    raise
        self._set_raw (obj, raw_value, value, changed)
    # end def set_raw

    def sync_cooked (self, obj, raw_value) :
        if __debug__ :
            print _T \
                ( "Trying to sync pending attribute %s of %s to `%s`"
                ) % (self.name, obj.name, raw_value)
        self.set_raw (obj, raw_value)
    # end def sync_cooked

    def _check_sanity (self, attr_type) :
        if __debug__ :
            default = getattr (attr_type, "raw_default", None)
            if (   default is not None
               and not isinstance (default, (str, unicode))
               ) :
                d = attr_type.as_string (default)
                if d == "" and default is not None :
                    d = "%s" % default
                raise ValueError \
                    ( """>>> %s.%s: got `%s` instead of "%s" as `raw_default`"""
                    % (attr_type, self.name, default, d)
                    )
    # end def _check_sanity

    def _get_computed (self, obj) :
        computed = self.attr.computed
        if TFL.callable (computed) :
            val = computed (obj)
            if val is not None :
                return self.attr.cooked (val)
    # end def _get_computed

    def _inc_changes (self, man, obj, value) :
        man.inc_changes ()
    # end def _inc_changes

    def _set_cooked (self, obj, value, changed = 42) :
        self._set_cooked_inner (obj, value, changed)
    # end def _set_cooked

    def _set_cooked_inner (self, obj, value, changed = 42) :
        if value is not None :
            try :
                value = self.attr.cooked (value)
            except StandardError, exc :
                ### print "%s: %s.%s, value `%s`" % (exc, obj, self.name, value)
                raise
        self._set_cooked_value (obj, value, changed)
    # end def _set_cooked_inner

    def _set_cooked_value (self, obj, value, changed = 42) :
        attr = self.attr
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = self.get_value (obj) != value
        if changed :
            self.inc_changes (obj._attr_man, obj, value)
            setattr (obj, attr.ckd_name, value)
    # end def _set_cooked_value

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        self._set_cooked_inner (obj, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        pass
    # end def _set_raw_inner

    def __cmp__ (self, other) :
        return cmp  (self.attr, getattr (other, "attr", other))
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.attr)
    # end def __hash__

    def __repr__ (self) :
        return "%s `%s`" % (self.attr.typ, self.name)
    # end def __repr__

# end class Kind

class _Raw_Value_Mixin_ (Kind) :
    """Mixin for keeping raw values of user-specified attributes."""

    needs_raw_value = True

    def get_raw (self, obj) :
        return getattr (obj, self.attr.raw_name, "")
    # end def get_raw

    def get_value (self, obj) :
        if obj._attr_man.needs_sync.get (self.name) :
            self._sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def has_substance (self, obj) :
        return self.get_raw (obj) not in ("", self.raw_default)
    # end def has_substance

    def _set_cooked (self, obj, value, changed = 42) :
        self._set_cooked_inner (obj, value, changed)
        self._set_raw_inner (obj, self.attr.as_string (value), value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if changed == 42 :
            ### if the caller didn't pass a (boolean) value, evaluate it here
            changed = raw_value != self.get_raw (obj)
        if changed :
            self.inc_changes  (obj._attr_man, obj, value)
        self.__super._set_raw (obj, raw_value, value, changed)
        self._set_raw_inner   (obj, raw_value, value, changed)
    # end def _set_raw

    def _set_raw_inner (self, obj, raw_value, value, changed = 42) :
        setattr (obj, self.attr.raw_name, raw_value)
    # end def _set_raw_inner

    def _sync (self, obj) :
        raw_value = self.get_raw (obj)
        value     = None
        if raw_value :
            try :
                value = self.attr.from_string (raw_value, obj, obj.globals ())
            except StandardError, exc :
                if __debug__ :
                    print exc
        self._set_cooked_inner (obj, value)
        obj._attr_man.needs_sync [self.name] = False
    # end def _sync

# end class _Raw_Value_Mixin_

class _DB_Attr_ (Kind) :
    """Attributes stored in DB."""

    save_to_db     = True
    record_changes = True

    def to_save (self, obj) :
        raw_val = self.get_raw (obj)
        result  = bool (raw_val)
        if result and not self.store_default :
            result = raw_val != self.raw_default
        return result
    # end def to_save

# end class _DB_Attr_

class _User_ (_DB_Attr_, Kind) :
    """Attributes set by user."""

    electric       = False

    def has_substance (self, obj) :
        return self.get_value (obj) not in (None, self.default)
    # end def has_substance

# end class _User_

class _System_ (Kind) :
    """Attributes set by system."""

    electric       = True

# end class _System_

class _DB_System_ (_DB_Attr_, _System_) :
    pass
# end class _DB_System_

class _Volatile_ (Kind) :
    """Attributes not stored in DB."""

    save_to_db     = False
    record_changes = False

    def to_save (self, obj) :
        return False
    # end def to_save

# end class _Volatile_

class _Cached_ (_Volatile_, _System_) :

    is_settable = False
    kind        = "cached"

    def _inc_changes (self, man, obj, value) :
        pass
    # end def _inc_changes

# end class _Cached_

class Primary (_User_) :
    """Primary attribute: must be defined at all times, used for (essential)
       primary key.
    """

    is_primary  = True
    kind        = "primary"

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( "\n".join
                ( ( _T ( "Primary attribute `%s.%s` cannot be assigned.")
                  , _T ("Use `set` or `set_raw` to change it.")
                  )
                )
            % (obj.type_name, self.name)
            )
    # end def __set__

    def to_save (self, obj) :
        return True
    # end def to_save

    def __delete__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Primary attribute `%s.%s` cannot be deleted")
            % (obj.type_name, self.name)
            )
    # end def __delete__

# end class Primary

class Link_Role (Primary) :
    """Link-role attribute must be defined at all times, used for (essential)
       primary key.
    """

# end class Link_Role

class Required (_User_) :
    """Required attribute: must be defined by the tool user."""

    kind        = "required"

    def to_save (self, obj) :
        return self.has_substance (obj)
    # end def to_save

# end class Required

class Optional (_User_) :
    """Optional attribute: if undefined, the `default` value is used, if any."""

    kind = "optional"

# end class Optional

class Internal (_DB_System_) :
    """Internal attribute: value is defined by some component of the tool."""

    kind = "internal"

# end class Internal

class Const (_Cached_) :
    """Constant attribute (has static default value that cannot be changed)."""

    kind        = "constant"

    def __set__ (self, obj, value) :
        raise AttributeError \
            ( _T ("Constant attribute `%s.%s` cannot be changed")
            % (obj.type_name, self.name)
            )
    # end def __set__

# end class Const

class Cached (_Cached_) :
    """Cached attribute: value is defined by some component of the tool, but
       not saved to DB.
    """

# end class Cached

class Sync_Cached (_Cached_) :
    """Cached attribute computed automatically when syncing. This kind can be
       used for attributes dependending on attributes of different objects,
       as long those don't change significantly between syncing --- use
       :class:`Computed` otherwise.
    """

    def sync (self, obj) :
        self._set_cooked (obj, self._get_computed (obj))
        obj._attr_man.needs_sync [self.name] = False
    # end def sync

    def get_raw (self, obj) :
        if obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_raw (obj)
    # end def get_raw

    def get_value (self, obj) :
        if obj._attr_man.needs_sync [self.name] :
            self.sync (obj)
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        self.__super.reset (obj)
        obj._attr_man.needs_sync [self.name] = True
    # end def reset

# end class Sync_Cached

class Auto_Cached (_Cached_) :
    """Cached attribute that is recomputed whenever it is accessed after one
       or more of the other attributes changed since the last recomputation.

       This kind must **not** be used if the value of the attribute depends
       on other objects (use :class:`Sync_Cached` or :class:`Computed` if
       that's the case).
    """

    def get_value (self, obj) :
        man = obj._attr_man
        if (  (man.total_changes != man.update_at_changes.get (self.name, -1))
           or self.attr.ckd_name not in obj.__dict__
           ) :
            val = self._get_computed (obj)
            if val is None :
                return
            self._set_cooked (obj, val)
            man.update_at_changes [self.name] = man.total_changes
        return self.__super.get_value (obj)
    # end def get_value

    def reset (self, obj) :
        obj._attr_man.update_at_changes [self.name] = -1
    # end def reset

# end class Auto_Cached

class Once_Cached (_Cached_) :
    """Cached attribute computed just once (a.k.a. computed constant).
       This kind can be used if the `constant` value that is computed depends
       on attributes of different objects, as longs as those don't change
       during the lifetime of this attribute's object.
    """

    def reset (self, obj) :
        val = self.get_value (obj)
        if val is None :
            val = self._get_computed (obj)
            self._set_cooked_inner   (obj, val, changed = True)
    # end def reset

# end class Once_Cached

class Cached_Role (_Cached_) :
    """Cached attribute automagically updated by association."""

    def reset (self, obj) :
        pass
    # end def reset

# end class Cached_Role

class Cached_Role_DFC (Cached_Role) :
    """Cached attribute normally updated by association but asking
       association for DFC_Link.
    """

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if result is None :
            assoc = getattr (obj.home_scope, self.attr.assoc)
            links = getattr (assoc, self.attr.name) (obj)
            if links :
                assert len (links) == 1
                result = getattr (links [0], self.attr.name)
        return result
    # end def get_value

# end class Cached_Role_DFC

class Computed (_Cached_) :
    """Computed attribute: the value is computed for each and every attribute
       access. This is quite inefficient and should only be used if
       :class:`Auto_Cached` or :class:`Sync_Cached` don't work.
    """

    kind        = "computed"

    def reset (self, obj) :
        pass
    # end def reset

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        default = self.attr.raw_default
        if default :
            raise TypeError \
                ( "%s is computed but has default %r "
                  "(i.e., `computed` will never be called)"
                % (attr_type, default)
                )
    # end def _check_sanity

# end class Computed

class Computed_Mixin (Kind) :
    """Mixin to compute attribute value if empty."""

    def get_value (self, obj) :
        result = self.__super.get_value (obj)
        if result is None :
            result = self._get_computed (obj)
        return result
    # end def get_value

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        default = self.attr.raw_default
        if default :
            raise TypeError \
                ( "%s is _Computed_ but has default %r "
                  "(i.e., `computed` will never be called)"
                % (attr_type, default)
                )
    # end def _check_sanity

# end class Computed_Mixin

class Sticky_Mixin (Kind) :
    """Mixin to reset attribute to default value whenever user enters empty
       value.
    """

    def _check_sanity (self, attr_type) :
        self.__super._check_sanity (attr_type)
        if not self.attr.raw_default :
            raise TypeError \
                ("%s is sticky but lacks `default`" % (attr_type, ))
    # end def _check_sanity

    def _set_cooked (self, obj, value, changed = 42) :
        if value is None :
            self.reset (obj)
        else :
            self.__super._set_cooked (obj, value, changed)
    # end def _set_cooked

    def _set_raw (self, obj, raw_value, value, changed = 42) :
        if raw_value in ("", None) :
            self.reset (obj)
        else :
            self.__super._set_raw (obj, raw_value, value, changed)
    # end def _set_raw

# end class Sticky_Mixin

### XXX Object-Reference- and Link-related kinds

if __name__ != "__main__" :
    MOM.Attr._Export ("*", "_Raw_Value_Mixin_")
### __END__ MOM.Attr.Kind
