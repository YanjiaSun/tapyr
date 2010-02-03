# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP._Person_has_Property_
#
# Purpose
#    Base class for link between Person and some other object
#
# Revision Dates
#     3-Feb-2010 (CT) Creation
#    ��revision-date�����
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP.Person  import Person

_Ancestor_Essence = MOM.Link2

class _Person_has_Property_ (PAP.Entity, _Ancestor_Essence) :
    """Base class for link between Person and some other object"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            role_type     = Person
            ui_name       = _("Person")
            auto_cache    = True

        # end class left

        class desc (A_String) :
            """Short description of the link"""

            kind          = Attr.Optional
            max_length     = 20
            ui_name        = _("Description")

        # end class desc

    # end class _Attributes

# end class _Person_has_Property_

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP._Person_has_Property_
