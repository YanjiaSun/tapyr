# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Picture
#
# Purpose
#    Model a picture that can be displayed on a web page
#
# Revision Dates
#    22-Mar-2010 (CT) Creation
#    13-Oct-2010 (CT) `example` added
#     5-Sep-2011 (CT) `width.max_value` increased from 1000 to 1200
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW                     import GTW

import _GTW._OMP._SWP.Gallery

from   _MOM._Attr.A_2D          import A_2D_Int, D2_Value_Int

from   _TFL                     import sos
from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = D2_Value_Int

class _Pic_ (_Ancestor_Essence) :
    """Model a picture"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class dir (A_String) :
            """Directory in gallery holding pictures."""

            kind               = Attr.Const
            default            = u"im"

        # end class dir

        class extension (A_String) :
            """Extension of file holding picture."""

            kind               = Attr.Const
            default            = u".jpg"

        # end class extension

        class height (_Ancestor.y) :
            """Height of picture."""

            max_value          = 1000
            min_value          = 200

        # end class height

        class path (A_String) :
            """Path of file holding picture."""

            kind               = Attr.Computed

            def computed (self, obj) :
                owner = obj.owner
                if owner :
                    p = sos.path.join \
                        (owner.gallery.directory, obj.dir, owner.name)
                    return p + obj.extension
            # end def computed

        # end class path

        class width (_Ancestor.x) :
            """Width of picture."""

            max_value          = 1200
            min_value          = 200

        # end class width

    # end class _Attributes

# end class _Pic_

_Ancestor_Essence = _Pic_

class _Thumb_ (_Ancestor_Essence) :
    """Model a thumbnail of a picture."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class dir (_Ancestor.dir) :
            """Directory in gallery holding thumbnails."""

            default            = u"th"
            example            = u"th"

        # end class dir

        class height (_Ancestor.height) :

            max_value          = 200
            min_value          = 50

        # end class height

        class width (_Ancestor.width) :

            max_value          = 200
            min_value          = 50

        # end class width

    # end class _Attributes

# end class _Thumb_

_Ancestor_Essence = GTW.OMP.SWP.Link1

class Picture (_Ancestor_Essence) :
    """Model a picture that can be displayed on a web page."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Gallery to which this picture belongs."""

            import _GTW._OMP._SWP.Gallery
            role_type          = GTW.OMP.SWP.Gallery

            auto_cache         = "pictures"

        # end class left

        class number (A_Int) :
            """Number of picture in gallery."""

            kind               = Attr.Primary
            check              = ("value >= 0", )

        # end class name

        ### Non-primary attributes

        class name (A_String) :

            kind               = Attr.Auto_Cached

            def computed (self, obj) :
                if obj.number is not None :
                    return "%4.4d" % obj.number
            # end def computed

        # end class name

        class photo (A_2D_Int) :
            """Picture."""

            kind               = Attr.Necessary
            P_Type             = _Pic_
            typ                = "Picture"

        # end class photo

        class thumb (A_2D_Int) :
            """Thumbnail"""

            kind               = Attr.Necessary
            P_Type             = _Thumb_
            typ                = "Thumbnail"

        # end class thumb

    # end class _Attributes

# end class Picture

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Picture
