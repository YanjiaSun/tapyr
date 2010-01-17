# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
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
#    GTW.NAV.Permission
#
# Purpose
#    Classes modelling permissions for accessing Navigation objects
#
# Revision Dates
#    16-Jan-2010 (CT) Creation
#    ��revision-date�����
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW.NAV

from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Filter

class _Permission_ (TFL._.Filter._Filter_S_) :

    pass

# end class _Permission_

class In_Group (_Permission_) :
    """Permission if user is member of group"""

    def __init__ (self, name) :
        self.name = name
    # end def __init__

    @property
    def group (self) :
        scope = GTW.NAV.Root.top.scope
        Group = scope ["Auth.Group"]
        return Group.instance (self.name)
    # end def group

    def predicate (self, user, page, * args, ** kw) :
        return self.group in user.groups
    # end def predicate

# end class In_Group

class In_Page_Group (_Permission_) :

    def predicate (self, user, page, * args, ** kw) :
        return page.Group in user.groups
    # end def predicate

# end class In_Page_Group

class Is_Creator (_Permission_) :

    def __init__ (self, attr_name = "creator") :
        self.attr_name = attr_name
    # end def __init__

    def predicate (self, user, page, * args, ** kw) :
        return user == getattr (page.obj, self.attr_name, None)
    # end def predicate

# end class Is_Creator

if __name__ != "__main__":
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Permission
