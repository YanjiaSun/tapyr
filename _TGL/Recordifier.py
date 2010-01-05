# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TGL.Recordifier
#
# Purpose
#    Provide classes supporting the conversion of formatted strings to records
#
# Revision Dates
#    17-Sep-2006 (CT) Creation
#    ��revision-date�����
#--

from   _TFL import TFL
from   _TGL import TGL

from   _TFL.Regexp import re

import _TFL.Caller
import _TFL.Record
import _TFL._Meta.Object

class _Recordifier_ (TFL.Meta.Object) :

    def __init__ (self, Result_Type) :
        self.Result_Type = Result_Type
    # end def __init__

    def __call__ (self, s) :
        conv   = self._converters
        result = self.Result_Type ()
        for k, v in self._field_iter (s) :
            setattr (result, k, conv [k] (v))
        return result
    # end def __call__

# end class _Recordifier_

class By_Regexp (_Recordifier_) :
    """Convert strings via regexp to records.

       >>> br = By_Regexp (
       ...   TFL.Regexp
       ...     (r"(?P<dt> (?P<y> \d{4})-(?P<m> \d{2})(?:-(?P<d> \d{2}))?)"
       ...      r" \s+ (?P<M> \d+) \s+ (?P<w> \d+\.\d*)", re.X)
       ...     , M = int, weight = float, y = int, m = int, d = int)
       >>> print br ("2006-06-01 6  96.4  1.20  93.5  98.1")
       (M = 6, d = 1, dt = 2006-06-01, m = 6, w = 96.4, y = 2006)
       >>> print br ("2006-06 6  96.4  1.20  93.5  98.1")
       (M = 6, dt = 2006-06, m = 6, w = 96.4, y = 2006)
    """

    field_pat = TFL.Regexp \
        ( r"\(\?P< (?P<name> [a-zA-Z_][a-zA-Z0-9_]*) >"
        , flags = re.VERBOSE
        )

    def __init__ (self, regexp, Result_Type = TFL.Record, ** converters) :
        self.__super.__init__ (Result_Type = Result_Type)
        self.regexp      = rex  = TFL.Regexp (regexp)
        self._converters = conv = {}
        for match in self.field_pat.search_iter (rex._pattern.pattern) :
            name = match.group ("name")
            conv [name] = \
                (  converters.get (name)
                or converters.get ("default_converter", str)
                )
    # end def __init__

    def _field_iter (self, s) :
        match  = self.regexp.search (s)
        if match :
            for k, v in match.groupdict ().iteritems () :
                if v is not None :
                    yield k, v
        else :
            raise ValueError, "`%s` doesn't match `%s`" % \
                (s, self.regexp._pattern.pattern)
    # end def _field_iter

# end class By_Regexp

class By_Separator (_Recordifier_) :
    """Convert strings by splitting on whitespace into records.

       >>> bw = By_Separator (
       ...   "d", ("m", int), "avg", "err", "min", "max",
       ...   _default_converter = float, d = str)
       >>> print bw ("2006-06-01 6  96.4  1.20  93.5  98.1")
       (avg = 96.4, d = 2006-06-01, err = 1.2, m = 6, max = 98.1, min = 93.5)
       >>> print bw ("2006-06-01 6  96.4  1.20  93.5")
       (avg = 96.4, d = 2006-06-01, err = 1.2, m = 6, min = 93.5)
       >>> print bw ("2006-06-01 6  96.4  1.20  93.5  98.1 42")
       (avg = 96.4, d = 2006-06-01, err = 1.2, m = 6, max = 98.1, min = 93.5)
    """

    _separator         = None
    _default_converter = str

    def __init__ (self, * fields, ** kw) :
        self.__super.__init__ \
            (Result_Type = kw.get ("Result_Type", TFL.Record))
        if "_separator" in kw :
            self._separator = kw ["_separator"]
        if "_default_converter" in kw :
            self._default_converter = kw ["_default_converter"]
        self._converters = conv = {}
        self._fields     = []
        add = self._fields.append
        for f in fields :
            if isinstance (f, str) :
                name    = f
                c       = kw.get (name, self._default_converter)
            else :
                name, c = f
            conv [name] = c
            add (name)
    # end def __init__

    def _field_iter (self, s) :
        for k, v in zip (self._fields, s.split ()) :
            yield k, v
    # end def _field_iter

# end class By_Separator

if __name__ == "__main__" :
    TGL._Export_Module ()
### __END__ TGL.Recordifier
