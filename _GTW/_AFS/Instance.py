# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
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
#    GTW.AFS.Instance
#
# Purpose
#    Model a AFS form instance plus the data for the form's entities and fields
#
# Revision Dates
#    25-Feb-2011 (CT) Creation
#    27-Feb-2011 (CT) Re-Creation (combine static and dynamic properties into
#                     a single object per form element)
#    28-Feb-2011 (CT) `needs_value` added
#     1-Mar-2011 (CT) `_Base_` factored
#    ��revision-date�����
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import base64
import hashlib
import json

class _Base_ (TFL.Meta.Object) :

    def form_hash (self, form_sig) :
        hash = hashlib.sha224 (str (form_sig)).digest ()
        return base64.b64encode (hash, ":-").rstrip ("=")
    # end def form_hash

    def form_sig (self, * args) :
        return tuple \
            (s for s in self.form_sig_iter (* args) if s is not None)
    # end def form_sig

    def form_sig_iter (self, arg1 = None, * args) :
        yield arg1
        yield self.prefilled
        for c in self.children :
            cig = c.elem._value_sig (c)
            yield cig
        for a in args :
            yield a
    # end def form_sig_iter

    def transitive_iter (self) :
        yield self
        for c in self.children :
            for x in c.transitive_iter () :
                yield x
    # end def transitive_iter

    def _v_repr (self, v, name) :
        if isinstance (v, dict) :
            result = "%r" % (sorted (v.iteritems ()), )
        else :
            result = "%r" % (v, )
            if result.startswith (("u'", 'u"')) :
                result = result [1:]
        return "%s-v = %s" % (name, result)
    # end def _v_repr

# end class _Base_

class Instance (_Base_) :
    """Model an instance of an AFS form element."""

    children = ()
    value    = None

    def __init__ (self, elem, ** kw) :
        self.pop_to_self  (kw, "children", "value")
        self.elem = elem
        self.kw   = kw
    # end def __init__

    @Once_Property
    def as_js (self) :
        return "new $GTW.AFS.Form (%s)" % (self.as_json)
    # end def as_js

    @Once_Property
    def as_json (self) :
        return json.dumps (self.as_json_cargo)
    # end def as_json

    @Once_Property
    def as_json_cargo (self) :
        result = self.elem.as_json_cargo
        result.update (self.kw)
        if self.children :
            result ["children"]  = [c.as_json_cargo for c in self.children]
        if self.value is not None :
            result ["value"]     = self.value
        if self.prefilled :
            result ["prefilled"] = True
        return result
    # end def as_json_cargo

    @property
    def init (self) :
        return self.value and self.value.get ("init", {})
    # end def init

    @property
    def prefilled (self) :
        if self.value :
            return self.value.get ("prefilled")
    # end def prefilled

    @property
    def sid (self) :
        return self.value and self.value.get ("sid")
    # end def sid

# end class Instance

if __name__ != "__main__" :
    GTW.AFS._Export ("Instance")
### __END__ GTW.AFS.Instance
