# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DWB.SQL.
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
#    MOM.DWB.SQL__Test
#
# Purpose
#    Base test during development
#
# Revision Dates
#    11-Feb-2010 (MG) Creation
#    ��revision-date�����
#--

from _MOM.__doc__ import *

### Because the example classes are all defined here and not in their
### own package namespace, we'll fake it
BMT._Export ("*", "Version")

from _MOM._EMS.SQL          import Manager as EMS
from _MOM._DBW._SQL.Manager import Manager     as DBW

apt = MOM.App_Type (u"BMT", BMT).Derived (EMS, DBW)

scope = MOM.Scope.new (apt, "sqlite:///:memory:")
#scope = MOM.Scope.new (apt, "sqlite:///test.sqlite")
m     = scope.BMT.Mouse   ("mouse")
r     = scope.BMT.Rat     ("rat")
t1   = scope.BMT.Trap     ("X", 1)
#t2   = scope.BMT.Trap     ("X", 2)

scope.BMT.Rodent_in_Trap (m, t1)
scope.BMT.Rodent_in_Trap (r, ("X", 2))
if 0 :
    c1 = MOM.SCM.Change.Attr (m, dict (color = "gray"))
    c2 = MOM.SCM.Change.Attr (m, dict (weight = "20"))
    c1.add_change (c2)
    scope.ems.register_change (c2)
    scope.ems.register_change (c1)

    #print scope.BMT.Rodent_in_Trap.query ().all ()
    csk = TFL.Sorted_By (Q.parent != None, Q.cid)
    for c in m.changes ().order_by (csk) : print c
### __END__ MOM.DWB.SQL__Test
