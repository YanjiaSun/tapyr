# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
#    GTW.Form.MOM._Instance_
#
# Purpose
#    Base class for form's which handle instances
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Error handling added
#    29-Jan-2010 (MG) Bug fixing
#    30-Jan-2010 (MG) Instance state added, bug fixing continued
#    30-Jan-2010 (MG) Instance state corrected, update roles only if they
#                     have been changed
#    ��revision-date�����
#--

from   _MOM               import MOM
import _MOM._Attr.Type

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _GTW                                 import GTW
import _GTW._Form._Form_
import _GTW._Form.Field
import _GTW._Form._MOM.Field_Group_Description

import _GTW._Tornado.Request_Data

import  base64
import  cPickle

MOM.Attr.A_Attr_Type.widget = "html/field.jnj, string"

class Instance_State_Field (GTW.Form.Field) :
    """Saves the state of the object to edit before the user made changes"""

    hidden = True

    widget = "html/field.jnj, hidden"

    def get_raw (self, instance) :
        state = {}
        form  = self.form
        for n, f in form.fields.iteritems () :
            state [n] = form.get_raw (f)
        return base64.b64encode (cPickle.dumps (state))
    # end def get_raw

# end class  Instance_State_Field

class M_Instance (TFL.Meta.Object.__class__) :
    """Meta class for MOM object forms"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.et_man :
            et_man                = cls.et_man
            cls.fields_for_et_man = TFL.defaultdict (list)
            cls.Roles             = []
            for fg in cls.field_groups :
                if isinstance (fg, GTW.Form.Field_Group) :
                    for f in fg.fields :
                        cls.fields_for_et_man [f.et_man].append (f)
            if issubclass (et_man._etype, MOM.Link) :
                ### handle the link role's before the link itself
                scope             = et_man.home_scope
                cls.Roles         = \
                    [   (r.name, getattr (scope, r.role_type.type_name))
                    for r in et_man.Roles
                    ]
    # end def __init__

    def New (cls, et_man, * field_group_descriptions, ** kw) :
        field_groups  = []
        suffix        = et_man.type_base_name
        if "suffix" in kw :
            suffix    = "__".join ((kw.pop ("suffix"), suffix))
        added_fields  = set ()
        if not field_group_descriptions :
            field_group_descriptions = \
                (GTW.Form.MOM.Field_Group_Description (), )
        for fgd in field_group_descriptions :
            field_groups.extend (fgd (et_man, added_fields))
        return cls.__m_super.New \
            ( suffix
            , field_groups = field_groups
            , et_man       = et_man
            , ** kw
            )
    # end def New

# end class M_Instance

class _Instance_ (GTW.Form._Form_) :
    """Base class for the real form and the `nested` from."""

    __metaclass__ = M_Instance
    et_man        = None

    def __init__ (self, instance = None, prefix = None, parent = None) :
        self.__super.__init__ (instance)
        self.instance_for_et_man = {self.et_man : instance}
        scope                    = self.et_man.home_scope
        for role_name, et_man in self.Roles :
            self.instance_for_et_man [et_man] = getattr \
                (instance, role_name, None)
        self.prefix              = prefix
        ### make copies of the inline groups to allow caching of inline forms
        self.inline_groups       = []
        for i, fg in enumerate (self.field_groups) :
            if isinstance (fg, GTW.Form.MOM.Inline) :
                self.field_groups [i] = new_fg = fg.clone (self)
                self.inline_groups.append (new_fg)
        self.parent              = parent
    # end def __init__

    def add_changed_raw (self, dict, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        raw       = self.get_raw            (field)
        old       = self.instance_state.get (field.name, u"")
        if raw != old :
            dict [field.name] = raw
    # end def add_changed_raw

    def _get_raw (self, field) :
        return field.get_raw (self.instance_for_et_man.get (field.et_man))
    # end def _get_raw

    @TFL.Meta.Once_Property
    def instance_state_field (self) :
        return Instance_State_Field \
            ( "instance_state"
            , et_man = self.et_man
            , form   = self
            )
    # end def instance_state_field

    @TFL.Meta.Once_Property
    def instance_state (self) :
        encoded = self.request_data.get \
            (self.get_id (self.instance_state_field))
        if encoded :
            return cPickle.loads (base64.b64decode (encoded))
        return {}
    # end def instance_state

    def __call__ (self, request_data) :
        ### XXX does not feel to be the correct place to make this conversion
        if not isinstance (request_data, GTW.Tornado.Request_Data) :
            request_data  = GTW.Tornado.Request_Data (request_data)
        self.request_data = request_data
        roles             = []
        for role_name, et_man in self.Roles :
            if self.parent and et_man is self.parent.et_man :
                instance  = self.parent.instance
            else :
                instance  = self._create_or_update (et_man, None)
            if instance :
                roles.append (instance and instance.epk_raw)
        if not self.errors and not self.field_errors :
            self.instance = self._create_or_update (self.et_man, roles, True)
        error_count       = len (self.errors) + len (self.field_errors)
        for ig in self.inline_groups :
            error_count  += ig (request_data)
        return error_count
    # end def __call__

    def _create_or_update (self, et_man, roles, required = False) :
        roles         = roles or ()
        has_substance = len (roles)
        raw_attrs     = {}
        instance      = self.instance_for_et_man [et_man]
        for f in self.fields_for_et_man [et_man] :
            value           = self.add_changed_raw (raw_attrs, f)
            #has_substance  += bool \
            #    (value and self.get_id (f) in self.request_data)
        if raw_attrs or roles and (len (roles) == len (self.Roles)) :
            errors = []
            ### at least on attribute is filled out
            try :
                raw_attrs ["on_error"] = errors.append
                if instance :
                    if et_man.Roles :
                        roles = dict \
                            (   (ak.name, r)
                            for (ak, r) in zip (et_man.Roles, roles)
                            )
                        curr = dict \
                            ((r, getattr (instance, r).epk_raw) for r in roles)
                        if curr != roles :
                            instance.set_raw \
                                (on_error = errors.append, ** roles)
                    if len (raw_attrs) > 1 :
                        instance.set_raw (** raw_attrs)
                else :
                    instance = et_man (raw = True, * roles, ** raw_attrs)
            except Exception, exc:
                errors.append (exc)
            self._handle_errors (errors)
        return instance
    # end def _create_or_update

    def _handle_errors (self, error_list) :
        for error_or_list in error_list :
            error_list = (error_or_list, )
            if isinstance (error_or_list, MOM.Error.Invariant_Errors) :
                error_list = error_or_list.args [0]
            for error in error_list :
                attributes = list (getattr (error, "attributes", ()))
                attr       = getattr       (error, "attribute", None)
                if attr :
                    attributes.append (attr)
                for attr in attributes :
                    name = self.fields [attr].html_name
                    self.field_errors [name].append (error)
                if not attributes :
                    self.errors.append (error)
    # end def _handle_errors

    @TFL.Meta.Once_Property
    def hidden_fields (self) :
        return [self.instance_state_field]
    # end def hidden_fields

# end class _Instance_

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM._Instance_
