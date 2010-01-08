# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.__init__
#
# Purpose
#    Model navigation on websites
#
# Revision Dates
#    18-Oct-2008 (CT) Creation (factored from DJO.Navigation)
#     8-Jan-2010 (CT) Moved from DJO to GTW
#    ��revision-date�����
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

NAV = Package_Namespace ()
GTW._Export ("NAV")

del Package_Namespace

### __END__ GTW.NAV.__init__
