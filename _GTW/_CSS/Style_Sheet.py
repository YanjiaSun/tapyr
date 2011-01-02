# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
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
#    GTW.CSS.Style_Sheet
#
# Purpose
#    Model a CSS style sheet
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#     1-Jan-2011 (CT) `Eval` added
#     2-Jan-2011 (CT) `_Eval` factored
#    ��revision-date�����
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS.Media

import _TFL._Meta.Object
import _TFL.Caller

def Parameters (* bases, ** kw) :
    """Model parameters for CSS rules and stylesheets, defined by `kw` and
       inherited from `bases`.
    """
    return type ("CSS_Parameters", bases, kw)
# end def Parameters

class Parameter_Scope (TFL.Caller.Object_Scope_Mutable) :
    """Encapsulate a CSS parameters class so that it is usable as context for
       `exec` of a file containing CSS.Style_Sheet declarations.
    """

    def __init__ (self, parameters) :
        self.__super.__init__ \
            (object = parameters, locls = dict (P = parameters))
        self.style_sheets = []
    # end def __init__

    def __setitem__ (self, key, value) :
        self.__super.__setitem__ (key, value)
        if isinstance (value, Style_Sheet) :
            self.style_sheets.append (value)
    # end def __setitem__

# end class Parameter_Scope

class M_Style_Sheet (TFL.Meta.Object.__class__) :
    """Meta class for `Style_Sheet`"""

# end class M_Style_Sheet

class Style_Sheet (TFL.Meta.Object) :
    """Model a CSS style sheet"""

    __metaclass__ = M_Style_Sheet

    _CSS_globs    = {}

    def __init__ (self, * rules, ** attrs) :
        self.rules   = list (rules)
        self.imports = list (attrs.pop ("imports", []))
        self.media   = attrs.pop ("media", None) or GTW.CSS.Media.Type ("all")
        self.name    = attrs.pop ("name",  None)
        self.attrs   = attrs
    # end def __init__

    def add_import (self, * imports) :
        self.imports.extend (imports)
    # end def add_import

    def add_rule (self, * rules) :
        self.rules.extend (rules)
    # end def add_rule

    @classmethod
    def Eval (cls, * fragments, ** kw) :
        return cls._Eval (fragments, ** kw)
    # end def Eval

    @classmethod
    def Read (cls, * file_names, ** kw) :
        """Read style sheets definitions from `file_names`."""
        def _gen (file_names) :
            for file_name in file_names :
                with open (file_name, "rt") as file :
                    yield file
        return cls._Eval (_gen (file_names), ** kw)
    # end def Read

    @classmethod
    def _Eval (cls, fragments, parameters) :
        scope = Parameter_Scope (parameters)
        globs = cls._get_CSS_globs ()
        for f in fragments :
            exec (f, globs, scope)
        return scope.style_sheets
    # end def _Eval

    @classmethod
    def _get_CSS_globs (cls) :
        result = cls._CSS_globs
        if not result :
            from _GTW._CSS import import_CSS
            result = cls._CSS_globs = import_CSS.__dict__
        return result
    # end def _get_CSS_globs

    def __iter__ (self) :
        for i in self.imports :
            for r in i :
                yield i
        for r in self.rules :
            for x in r :
                yield x
    # end def __iter__

    def __str__ (self) :
        return "\n\n".join (str (r) for r in self)
    # end def __str__

# end class Style_Sheet

S = Style_Sheet

__all__ = tuple \
    ( k for (k, v) in globals ().iteritems () if isinstance (v, M_Style_Sheet)
    ) + ("Parameters", )

if __name__ != "__main__" :
    GTW.CSS._Export (* __all__)
### __END__ GTW.CSS.Style_Sheet