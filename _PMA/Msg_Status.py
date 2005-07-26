# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.Msg_Status
#
# Purpose
#    Encapsulate status of mail message
#
# Revision Dates
#     4-Jan-2005 (CT) Creation
#    25-Jul-2005 (CT) `new` and `_Table` added (plus `load` and `save`)
#    25-Jul-2005 (CT) `_Status_` factored
#    26-Jul-2005 (CT) `load` and `save` moved back in here from `_Status_`
#    ��revision-date�����
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
import _PMA._Status_

import cPickle                 as     pickle

import time

class Msg_Status (PMA._Status_) :
    """Status of mail message"""

    first_read = property (lambda s : s._attr.get ("first_read"))
    last_read  = property (lambda s : s._attr.get ("last_read"))
    unseen     = property (lambda s : s.first_read is None)

    _Table     = {}

    @classmethod
    def load (cls, filename) :
        try :
            f = open (filename)
        except IOError :
            pass
        else :
            try :
                try :
                    cls._Table = pickle.load (f)
                except EOFError :
                    pass
            finally :
                f.close ()
    # end def load

    @classmethod
    def new (cls, name) :
        result = cls._Table.get (name)
        if result is None :
            result = cls._Table [name] = cls ()
        return result
    # end def new

    @classmethod
    def save (cls, filename) :
        f = open    (filename, "wb")
        pickle.dump (cls._Table, f, pickle.HIGHEST_PROTOCOL)
        f.close     ()
    # end def save

    def set_read (self, t = None) :
        if t is None :
            t = time.time ()
        _attr = self._attr
        if self.unseen :
            _attr ["first_read"] = t
        _attr ["last_read"] = t
        return t
    # end def set_read

# end class Msg_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Msg_Status
