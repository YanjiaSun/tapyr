# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Form.Field
#
# Purpose
#    A field of a form
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    02-Feb-2010 (MG) `get_raw` paremeter form added
#    ��revision-date�����
#--
from   _TFL               import TFL
import _TFL._Meta.Object
from   _GTW               import GTW
import _GTW._Form

class Field (TFL.Meta.Object) :
    """A free field which should be part of a HTML form"""

    widget = "html/field.jnj, string"
    hidden = False

    def __init__ (self, name, default = "", ** kw) :
        self.name      = name
        self.html_name = name
        self.default   = default
        self.__dict__.update (kw)
    # end def __init__

    def get_raw (self, form, obj) :
        return getattr (obj, self.name, self.default)
    # end def get_raw

# end class Field

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field
