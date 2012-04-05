# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Tornado.
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
#    GTW.Tornado.Error
#
# Purpose
#    Define special error exceptions
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    14-Jan-2010 (CT) s/Templeteer/Templateer/g
#    15-Jan-2010 (CT) s/HTTP_Status/Status/
#    15-Jan-2010 (CT) `M_Status` added
#    18-Jan-2010 (CT) Use `Templateer.get_std_template` instead of homegrown
#                     code
#    17-Aug-2010 (CT) `Error_503` added
#    31-Dec-2010 (CT) s/get_std_template/get_template/
#     2-May-2011 (CT) `Error_400` added
#    27-May-2011 (CT) `Error_405.__init__` redefined to accept `valid_methods`
#     5-Apr-2012 (CT) Remove assignment to `handler.request.user`
#    ��revision-date�����
#--

from   _GTW              import GTW
from   _TFL              import TFL

import _GTW._Tornado
import _TFL._Meta.Object

from    tornado.web      import HTTPError

class M_Status (TFL.Meta.Object.__class__) :
    """Meta class for Status"""

    Table         = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.status_code is not None :
            cls.Table [cls.status_code] = cls
    # end def __init__

# end class M_Status

class Status (HTTPError, TFL.Meta.Object) :
    """Base class for HTTP status exceptions"""

    __metaclass__ = M_Status

    status_code   = None

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (self.status_code, * args, ** kw)
    # end def __init__

# end class Status

class _Redirect_ (Status) :
    """Base class for all redirect's"""

    def __init__ (self, url, * args, ** kw) :
        self.url = url
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def __call__ (self, handler, nav_root = None) :
        handler.redirect (self.url, self.status_code == 301)
        return True ### exception handled
    # end def __call__

# end class _Redirect_

### http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

class Redirect_301 (_Redirect_) :
    """Moved Permanently."""
    status_code = 301
# end class Redirect_301

class Redirect_302 (_Redirect_) :
    """Found (moved temporarily)."""
    status_code = 302
# end class Redirect_302

class Redirect_303 (_Redirect_) :
    """See other."""
    status_code = 303
# end class Redirect_303

class Redirect_304 (_Redirect_) :
    """Not Modified."""
    status_code = 304
# end class Redirect_304

class Redirect_307 (_Redirect_) :
    """Temporary Redirect."""
    status_code = 307
# end class Redirect_307

class _Error_ (Status) :
    """Base class for all error responses."""

    def __call__ (self, handler, nav_root = None) :
        if nav_root :
            Templateer           = nav_root.Templateer
            template             = Templateer.get_template (self.status_code)
            context              = Templateer.Context \
                ( exception = self
                , page      = nav_root
                , nav_page  = nav_root
                , NAV       = nav_root
                , request   = handler.request
                )
            if handler._headers_written :
                if not handler._finished :
                    handler.finish ()
                return
            handler.clear          ()
            handler.set_status     (self.status_code)
            handler.finish         (template.render (context))
            return True
        return False ### trigger the default error exception handling code
    # end def __call__

# end class _Error_

class Error_400 (_Error_) :
    """Bad Request."""
    status_code = 400
# end class Error_400

class Error_401 (_Error_) :
    """Unauthorized."""
    status_code = 401
# end class Error_401

class Error_403 (_Error_) :
    """Forbidden."""
    status_code = 403
# end class Error_403

class Error_404 (_Error_) :
    """Not Found."""
    status_code = 404
# end class Error_404

class Error_405 (_Error_) :
    """Method Not Allowed."""

    status_code = 405

    def __init__ (self, * args, ** kw) :
        self.valid_methods = kw.pop ("valid_methods", None)
        self.__super.__init__ (* args, ** kw)
    # end def __init__

# end class Error_405

class Error_408 (_Error_) :
    """Request Timeout."""
    status_code = 408
# end class Error_408

class Error_409 (_Error_) :
    """Conflict."""
    status_code = 409
# end class Error_409

class Error_500 (_Error_) :
    """Internal Server Error."""
    status_code = 500
# end class Error_500

class Error_503 (_Error_) :
    """Service Unavailable."""
    status_code = 503
# end class Error_503

if __name__ != "__main__" :
    GTW.Tornado._Export ("*", "_Redirect_")
### __END__ GTW.Tornado.Error
