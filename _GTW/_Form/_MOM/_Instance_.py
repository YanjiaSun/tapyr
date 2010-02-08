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
#     2-Feb-2010 (MG) Collect all `Media`s from the field_group_descriptions
#                     and add the combined Media to the form class
#     2-Feb-2010 (MG) `_get_raw`: pass form to `field.get_raw`
#     2-Feb-2010 (MG) Instance state handling changed (field is now added to
#                     the first field group)
#                     `_create_or_update`: filter hidden field
#                     `hidden_fields` removed
#     3-Feb-2010 (MG) `New`: filter empty field groups
#     3-Feb-2010 (MG) Collect `Media`s of field groups instead of field group
#                     descriptions
#     3-Feb-2010 (MG) `_prepare_form` added
#     3-Feb-2010 (MG) Collect all completers and add the `js_on_ready` to the
#                     Media
#     5-Feb-2010 (MG) Handling of inline forms changed, handling of link
#                     creation changed
#     5-Feb-2010 (MG) Form class setup moved from `New` to `__new__`,
#                     `form_path` added
#     8-Feb-2010 (MG) Directly access the `_etype` of the `et_man` (An_Entity
#                     etype managers work differently)
#                     `__call__?: if `Attribute_Inline` set the
#                     created/modified instance to the main instance
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
import  itertools

class Instance_State_Field (GTW.Form.Field) :
    """Saves the state of the object to edit before the user made changes"""

    hidden = True

    widget = GTW.Form.Widget_Spec ("html/field.jnj, hidden")

    def get_raw (self, form, instance) :
        state = {}
        for n, f in form.fields.iteritems () :
            if not f.hidden :
                state [n] = form.get_raw (f)
        return base64.b64encode (cPickle.dumps (state))
    # end def get_raw

    def decode (self, data) :
        if data :
            return cPickle.loads (base64.b64decode (data))
        return {}
    # end def decode

# end class  Instance_State_Field

class M_Instance (GTW.Form._Form_.__class__) :
    """Meta class for MOM object forms"""

    parent_form  = None

    def __new__ (mcls, name, bases, dct) :
        et_man                   = dct.get ("et_man", None)
        field_group_descriptions = dct.pop ("field_group_descriptions", ())
        result = super (M_Instance, mcls).__new__ (mcls, name, bases, dct)
        if et_man :
            result.sub_forms = sub_forms = {}
            field_groups     = []
            medias           = []
            added            = set ()
            if not field_group_descriptions :
                ### XXX try to get the default field group descriptions for this
                ### et-man from somewhere
                field_group_descriptions = \
                    (GTW.Form.MOM.Field_Group_Description (), )
            for fgd in field_group_descriptions :
                fgs = [   fg
                      for fg in fgd (et_man, added, parent_form = result) if fg
                      ]
                field_groups.extend (fgs)
                for fg in fgs :
                    media = fg.Media
                    if media :
                        medias.append (media)
                    sub_form = getattr (fg, "form_cls", None)
                    if sub_form :
                        tbn = sub_form.et_man._etype.type_base_name
                        sub_forms [tbn] = sub_form
            result.add_internal_fields    (et_man, field_groups)
            result.Media        = GTW.Media.from_list (medias)
            result.field_groups = field_groups
            result.fields       = result._setup_fields (field_groups)
        return result
    # end def __new__

    def add_internal_fields (cls, et_man, field_groups) :
        ### we add the instance state field
        fg = field_groups [0]
        cls.instance_state_field = Instance_State_Field \
            ("instance_state", et_man = et_man)
        fg.fields.append (cls.instance_state_field)
    # end def add_internal_fields

    @TFL.Meta.Once_Property
    def form_path (cls) :
        tbn = cls.et_man._etype.type_base_name
        if cls.parent_form :
            return "%s/%s" % (cls.parent_form.form_path, tbn)
        return tbn
    # end def form_path

    def New (cls, et_man, * field_group_descriptions, ** kw) :
        suffix        = et_man._etype.type_base_name
        if "suffix" in kw :
            suffix    = "__".join ((kw.pop ("suffix"), suffix))
        return cls.__m_super.New \
            ( suffix
            , field_group_descriptions = field_group_descriptions
            , et_man                   = et_man
            , ** kw
            )
    # end def New

# end class M_Instance

class _Instance_ (GTW.Form._Form_) :
    """Base class for the form's handling any kind of MOM instances."""

    __metaclass__ = M_Instance
    et_man        = None
    error_count   = 0
    prototype     = False

    def __init__ (self, instance = None, prefix = None, parent = None) :
        self.__super.__init__ (instance)
        scope                    = self.et_man.home_scope
        self.prefix              = prefix
        self.parent              = parent
        ### make copies of the inline groups to allow caching of inline forms
        self.inline_groups       = []
        for i, fg in enumerate (self.field_groups) :
            if isinstance (fg, GTW.Form.MOM._Inline_) :
                self.field_groups [i] = new_fg = fg.clone (self)
                self.inline_groups.append (new_fg)
    # end def __init__

    def add_changed_raw (self, dict, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        raw       = self.get_raw            (field)
        old       = self.instance_state.get (field.name, u"")
        if raw != old :
            dict [field.name] = raw
    # end def add_changed_raw

    def _create_or_update (self, add_attrs = {}) :
        raw_attrs     = dict (add_attrs)
        instance      = self.instance
        for f in (f for f in self.fields if not f.hidden) :
            value     = self.add_changed_raw (raw_attrs, f)
        if raw_attrs :
            errors = []
            ### at least on attribute is filled out
            try :
                raw_attrs ["on_error"] = errors.append
                if instance :
                    instance.set_raw (** raw_attrs)
                else :
                    instance = self.et_man (raw = True, ** raw_attrs)
            except Exception, exc:
                if __debug__ :
                    import traceback
                    ## traceback.print_exc ()
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
    def instance_state (self) :
        return self.instance_state_field.decode \
            (self.request_data.get (self.get_id (self.instance_state_field)))
    # end def instance_state

    def _prepare_form (self) :
        return True
    # end def _prepare_form

    def __call__ (self, request_data) :
        #if getattr (self, "_break", False) :
        #    import pdb; pdb.set_trace ()
        self.request_data = request_data
        if not self._prepare_form () :
            ### this form does not need any further processing
            return 0
        self.instance = self._create_or_update  ()
        error_count   = len (self.errors) + len (self.field_errors)
        if not error_count :
            for ig in self.inline_groups :
                error_count  += ig (request_data)
                if (   not error_count
                   and isinstance (ig, GTW.Form.MOM.Attribute_Inline)
                   ) :
                    setattr (self.instance, ig.link_name, ig.instance)
        self.error_count      = error_count
        return error_count
    # end def __call__

# end class _Instance_

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM._Instance_
