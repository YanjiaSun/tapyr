# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.RST
#
# Purpose
#    Test RESTful api
#
# Revision Dates
#    27-Jun-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

from   _MOM.import_MOM          import *
from   _MOM.Product_Version     import Product_Version, IV_Number

from   _TFL                     import sos
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property
from   _TFL.I18N                import _, _T, _Tn

from   _TFL.Formatter           import Formatter, formatted_1

formatted = Formatter (width = 240)

import _GTW._Werkzeug.Command_X

import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM

import datetime
import json

GTW.Version = Product_Version \
    ( productid           = u"MOM/GTW Test Cases"
    , productnick         = u"MOM-Test"
    , productdesc         = u"Test application for the regressiontest"
    , date                = "27-Jun-2012 "
    , major               = 0
    , minor               = 2
    , patchlevel          = 0
    , author              = u"Martin Glueck/Christian Tanzer"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("MOMT", )
        , ("MOMT", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".momt"
        )
    )

_Ancestor = GTW.Werkzeug.Command_X

class _GTW_Test_Command_ (_Ancestor) :

    _rn_prefix            = "_GTW_Test"

    ANS                   = GTW
    nick                  = u"MOMT"
    default_db_name       = "test"
    PNS_Aliases           = dict \
        ( PAP             = GTW.OMP.PAP
        , SRM             = GTW.OMP.SRM
        , SWP             = GTW.OMP.SWP
        )

    SALT                  = bytes \
        ( "ohQueiro7theG4vai9shi4oi9iedeethaeshooqu7oThi9Eecephaj")

    _defaults               = dict \
        ( config            = "~/.gtw-test.config"
        , fixtures          = "yes"
        , port              = 9090
        , UTP               = "RST"
        )

    Backend_Parameters    = dict \
        ( HPS             = "'hps://'"
        , SQL             = "'sqlite://'"
        , POS             = "'postgresql://regtest:regtest@localhost/regtest'"
        , MYS             = "'mysql://:@localhost/test'"
        , MYST            = "'mysql://:@localhost/test?unix_socket=/var/run/mysqld/mysqld-ram.sock'"
        )

    Backend_Default_Path  = dict \
        ( (k, None) for k in Backend_Parameters)

    def combiner (self, backends, bpt) :
        if bpt > 1 :
            backends = backends + [backends [0]]
        return TFL.window_wise (backends, bpt)
    # end def combiner

    def create_rst (self, cmd, app_type, db_url, ** kw) :
        from _GTW._RST import MOM as R_MOM
        result = GTW.RST.Root \
            ( App_Type          = app_type
            , DB_Url            = db_url
            , DEBUG             = True
            , encoding          = cmd.output_encoding
            , HTTP              = cmd.HTTP
            , input_encoding    = cmd.input_encoding
            , language          = "de"
            , entries           = [R_MOM.Scope (name = "v1")]
            , ** kw
            )
        if cmd.log_level :
            print (formatted (result.Table))
        return result
    # end def create_rst

    def create_test_dict ( self, test_spec
                         , backends = None
                         , bpt      = 1
                         , combiner = None
                         , ignore   = set ()
                         ) :
        result = {}
        if backends is None :
            backends = sos.environ.get ("GTW_test_backends", ("HPS:SQL"))
            if backends == "*" :
                backends = sorted (self.Backend_Parameters)
            else :
                backends = list (p.strip () for p in backends.split (":"))
        if combiner is None :
            combiner = self.combiner
        if isinstance (ignore, basestring) :
            ignore   = set ((ignore, ))
        elif not isinstance (ignore, set) :
            ignore   = set (ignore)
        if not isinstance (test_spec, dict) :
            test_spec = {"" : test_spec}
        for w in combiner ((b for b in backends if b not in ignore), bpt) :
            for name, code in test_spec.iteritems () :
                key = "_".join (p for p in (name, ) + w if p)
                result [key] = code % dict (self._backend_spec (w))
        return result
    # end def create_test_dict

    def fixtures (self, scope) :
        PAP   = scope.PAP
        SRM   = scope.SRM
        BiR   = SRM.Boat_in_Regatta
        ct    = PAP.Person ("Tanzer", "Christian")
        lt    = PAP.Person ("Tanzer", "Laurens", "William")
        cat   = PAP.Person ("Tanzer", "Clarissa", "Anna")
        ct_s  = SRM.Sailor (ct,  nation = "AUT", mna_number = "29676")
        lt_s  = SRM.Sailor (lt,  nation = "AUT", raw = True)
        cat_s = SRM.Sailor (cat, nation = "AUT", raw = True)
        opti  = SRM.Boat_Class ("Optimist", max_crew = 1)
        b     = SRM.Boat ("Optimist", "AUT", 1107)
        ys    = SRM.Handicap ("Yardstick")
        rev   = SRM.Regatta_Event \
            (u"Himmelfahrt", dict (start = u"20080501"), raw = True)
        reg   = SRM.Regatta_C (rev, opti)
        reh   = SRM.Regatta_H (rev, ys)
        bir   = SRM.Boat_in_Regatta (b, reg, skipper = lt_s)
        scope.commit ()
    # end def fixtures

    @Once_Property
    def jnj_src (self) :
        return "/tmp/test"
    # end def jnj_src

    def scope (self, * args, ** kw) :
        verbose = kw.pop ("verbose", True)
        return self.__super.scope (* args, verbose = verbose, ** kw)
    # end def scope

    @Once_Property
    def web_src_root (self) :
        return "/tmp/test"
    # end def web_src_root

    def _backend_spec (self, backends) :
        i = 0
        for b in backends :
            i += 1
            path = self.Backend_Default_Path [b]
            for k, v in zip \
                    ( ("p",                        "n",  "BN")
                    , (self.Backend_Parameters [b], path, repr (b))
                    ) :
                yield ("%s%d" % (k, i), v)
    # end def _backend_spec

    def _wsgi_app (self, cmd) :
        self._handle_create (cmd)
        result = self.__super._wsgi_app (cmd)
        return result
    # end def _wsgi_app

_Command_  = _GTW_Test_Command_ # end class

Scaffold   = _Command_ ()
Scope      = Scaffold.scope

from   posixpath import join as pjoin

import multiprocessing
import requests
import subprocess
import sys
import time

def _run_server (args = []) :
    print (["run_server"] + server_args + args)
    result = Scaffold (["run_server"] + server_args + args)
    return result
# end def run_server

def run_server (db_url = "hps://", db_name = None) :
    import tempfile
    cmd = \
        [ sys.executable, "-c"
        , "; ".join
            ( ( "from _GTW.__test__ import RST"
              , "RST.Scaffold "
              + "( "
              + repr
                  ( ["run_server"]
                  + server_args
                  + ["-db_url", db_url, "-db_name", db_name or "test"]
                  )
              + ")"
              )
            )
        ]
    ### print (cmd)
    p = subprocess.Popen (cmd, stderr = tempfile.TemporaryFile ())
    import socket
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    i = 0
    while True :
        try :
            s.connect (("localhost", 9999))
        except socket.error :
            if i < 20 :
                i += 1
                time.sleep (1)
        else :
            s.close ()
            break
    return p
# end def run_server

def _normal (k, v) :
    if k in ("date", "last-modified") :
        v = "<datetime instance>"
    elif k in ("etag",) :
        v = "ETag value"
    elif k == "content-length" :
        v = "<length>"
    return k, v
# end def _normal

def show (r) :
    output = formatted \
        ( dict
            ( headers = dict
                (_normal (k, v) for k, v in r.headers.iteritems ())
            , json    = r.json if r.content else None
            , status  = r.status_code
            , url     = r.url
            )
        )
    print (output)
    return r
# end def show

def traverse (url, level = 0) :
    rg    = requests.get     (url)
    ro    = requests.options (url)
    path  = requests.utils.urlparse (url).path or "/"
    if ro.ok :
        print (path, ":", ro.headers ["allow"], )
    else :
        print (path, ":", ro.status_code, r.content)
    if rg.ok and rg.content and rg.json :
        l = level + 1
        for e in rg.json.get ("entries", ()) :
            traverse (pjoin (url, str (e)), l)
# end def traverse

server_args = \
    [ "-UTP=RST"
    , "-auto_reload=no"
    , "-debug=yes"
    , "-load_I18N=no"
    , "-log_level=0"
    , "-port=9999"
    ]

### �text� ### The doctest follows::

_test_cqf = r"""
    >>> server = Scaffold (["wsgi"] + server_args + ["-db_url", %(p1)s, "-db_name", %(n1)s or "test"]) # doctest:+ELLIPSIS
    Loaded Scope...
    >>> root   = Scaffold.root
    >>> v1     = root.resource_from_href ("v1")

    >>> for e in v1.entries :
    ...     print ("%%s\n    %%s" %% (e.name, e.change_query_filters))
    MOM.Id_Entity
        ()
    MOM.Link
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM.Link1
        (Q.type_name.in_ (['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM._MOM_Link_n_
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    MOM.Link2
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    MOM.Object
        (Q.type_name.in_ (['PAP.Address', 'PAP.Company', 'PAP.Email', 'PAP.Person', 'PAP.Phone', 'SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event', 'SWP.Gallery', 'SWP.Page'],),)
    PAP.Address
        (Q.type_name == PAP.Address,)
    PAP.Subject
        (Q.type_name.in_ (['PAP.Company', 'PAP.Person'],),)
    PAP.Company
        (Q.type_name == PAP.Company,)
    PAP.Email
        (Q.type_name == PAP.Email,)
    PAP.Phone
        (Q.type_name == PAP.Phone,)
    PAP.Person
        (Q.type_name == PAP.Person,)
    PAP.Subject_has_Property
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone'],),)
    PAP.Subject_has_Address
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Person_has_Address'],),)
    PAP.Company_has_Address
        (Q.type_name == PAP.Company_has_Address,)
    PAP.Subject_has_Email
        (Q.type_name.in_ (['PAP.Company_has_Email', 'PAP.Person_has_Email'],),)
    PAP.Company_has_Email
        (Q.type_name == PAP.Company_has_Email,)
    PAP.Subject_has_Phone
        (Q.type_name.in_ (['PAP.Company_has_Phone', 'PAP.Person_has_Phone'],),)
    PAP.Company_has_Phone
        (Q.type_name == PAP.Company_has_Phone,)
    PAP.Entity_created_by_Person
        (Q.type_name == PAP.Entity_created_by_Person,)
    PAP.Person_has_Address
        (Q.type_name == PAP.Person_has_Address,)
    PAP.Person_has_Email
        (Q.type_name == PAP.Person_has_Email,)
    PAP.Person_has_Phone
        (Q.type_name == PAP.Person_has_Phone,)
    SRM.Link1
        (Q.type_name.in_ (['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team'],),)
    SRM.Link2
        (Q.type_name.in_ (['SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    SRM.Object
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event'],),)
    SRM._Boat_Class_
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Handicap'],),)
    SRM.Boat_Class
        (Q.type_name == SRM.Boat_Class,)
    SRM.Handicap
        (Q.type_name == SRM.Handicap,)
    SRM.Boat
        (Q.type_name == SRM.Boat,)
    SRM.Club
        (Q.type_name == SRM.Club,)
    SRM.Regatta_Event
        (Q.type_name == SRM.Regatta_Event,)
    SWP.Link1
        (Q.type_name.in_ (['SWP.Clip_O', 'SWP.Picture'],),)
    SWP.Object
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP.Object_PN
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP.Page
        (Q.type_name == SWP.Page,)
    SWP.Page_Y
        (Q.type_name == SWP.Page_Y,)
    SWP.Clip_O
        (Q.type_name == SWP.Clip_O,)
    SWP.Clip_X
        (Q.type_name == SWP.Clip_X,)
    SWP.Gallery
        (Q.type_name == SWP.Gallery,)
    SWP.Picture
        (Q.type_name == SWP.Picture,)
    SRM.Page
        (Q.type_name == SRM.Page,)
    SRM.Regatta
        (Q.type_name.in_ (['SRM.Regatta_C', 'SRM.Regatta_H'],),)
    SRM.Regatta_C
        (Q.type_name == SRM.Regatta_C,)
    SRM.Regatta_H
        (Q.type_name == SRM.Regatta_H,)
    SRM.Sailor
        (Q.type_name == SRM.Sailor,)
    SRM.Boat_in_Regatta
        (Q.type_name == SRM.Boat_in_Regatta,)
    SRM.Race_Result
        (Q.type_name == SRM.Race_Result,)
    SRM.Team
        (Q.type_name == SRM.Team,)
    SRM.Crew_Member
        (Q.type_name == SRM.Crew_Member,)
    SRM.Team_has_Boat_in_Regatta
        (Q.type_name == SRM.Team_has_Boat_in_Regatta,)

"""

_test_delete = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid/"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '13'
        }
    , 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            , 4
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            ]
        , 'url_template' : '/v1/MOM.Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (requests.delete ("http://localhost:9999/v1/pid/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'error' : "You need to send the object's `cid` with the request"
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (requests.delete ("http://localhost:9999/v1/pid/1", params = dict (cid = 2)))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'error' : 'Cid mismatch: requested cid = 2, current cid = 1'
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=2'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid?count"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '13'
        }
    , 'json' :
        { 'count' : 13 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (requests.delete ("http://localhost:9999/v1/pid/1", params = dict (cid = 1)))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'status' : 'Object with pid None successfully deleted'
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid?count"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '15'
        }
    , 'json' :
        { 'count' : 11 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (requests.delete ("http://localhost:9999/v1/pid/1", params = dict (cid = 1)))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'text/html'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'text/html'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '15'
        }
    , 'json' :
        { 'entries' :
            [ 2
            , 3
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            ]
        , 'url_template' : '/v1/MOM.Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid'
    }

    >>> server.terminate ()

"""

_test_get = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> r = show (requests.options ("http://localhost:9999"))
    { 'headers' :
        { 'allow' : 'GET, HEAD, OPTIONS'
        , 'content-length' : '<length>'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (requests.head ("http://localhost:9999"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' : None
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (requests.get ("http://localhost:9999"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' : [ 'v1' ]
        , 'url_template' : '/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (requests.get ("http://localhost:9999?verbose"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' : [ '/v1' ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/?verbose'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'entries' :
            [ 'MOM.Id_Entity'
            , 'MOM.Link'
            , 'MOM.Link1'
            , 'MOM._MOM_Link_n_'
            , 'MOM.Link2'
            , 'MOM.Object'
            , 'PAP.Address'
            , 'PAP.Subject'
            , 'PAP.Company'
            , 'PAP.Email'
            , 'PAP.Phone'
            , 'PAP.Person'
            , 'PAP.Subject_has_Property'
            , 'PAP.Subject_has_Address'
            , 'PAP.Company_has_Address'
            , 'PAP.Subject_has_Email'
            , 'PAP.Company_has_Email'
            , 'PAP.Subject_has_Phone'
            , 'PAP.Company_has_Phone'
            , 'PAP.Entity_created_by_Person'
            , 'PAP.Person_has_Address'
            , 'PAP.Person_has_Email'
            , 'PAP.Person_has_Phone'
            , 'SRM.Link1'
            , 'SRM.Link2'
            , 'SRM.Object'
            , 'SRM._Boat_Class_'
            , 'SRM.Boat_Class'
            , 'SRM.Handicap'
            , 'SRM.Boat'
            , 'SRM.Club'
            , 'SRM.Regatta_Event'
            , 'SWP.Link1'
            , 'SWP.Object'
            , 'SWP.Object_PN'
            , 'SWP.Page'
            , 'SWP.Page_Y'
            , 'SWP.Clip_O'
            , 'SWP.Clip_X'
            , 'SWP.Gallery'
            , 'SWP.Picture'
            , 'SRM.Page'
            , 'SRM.Regatta'
            , 'SRM.Regatta_C'
            , 'SRM.Regatta_H'
            , 'SRM.Sailor'
            , 'SRM.Boat_in_Regatta'
            , 'SRM.Race_Result'
            , 'SRM.Team'
            , 'SRM.Crew_Member'
            , 'SRM.Team_has_Boat_in_Regatta'
            ]
        , 'url_template' : '/v1/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1'
    }

    >>> rp = show (requests.get ("http://localhost:9999/v1/PAP.Person"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '3'
        }
    , 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            ]
        , 'url_template' : '/v1/PAP.Person/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/PAP.Person?verbose"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '3'
        }
    , 'json' :
        { 'entries' :
            [ { 'attributes' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              }
            , { 'attributes' :
                  { 'first_name' : 'Laurens'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'William'
                  , 'title' : ''
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'PAP.Person'
              }
            , { 'attributes' :
                  { 'first_name' : 'Clarissa'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'Anna'
                  , 'title' : ''
                  }
              , 'cid' : 3
              , 'pid' : 3
              , 'type_name' : 'PAP.Person'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person?verbose'
    }

    >>> for pid in rp.json ["entries"] :
    ...     _ = show (requests.get (pjoin (rp.url, str (pid))))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person/1'
    }
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '2'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Laurens'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'William'
            , 'title' : ''
            }
        , 'cid' : 2
        , 'pid' : 2
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person/2'
    }
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Clarissa'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'Anna'
            , 'title' : ''
            }
        , 'cid' : 3
        , 'pid' : 3
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person/3'
    }

    >>> r = show (requests.head ("http://localhost:9999/v1/PAP.Person/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' : None
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person/1'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP.Person/1'
    }

    >>> last_modified = r.headers ["last-modified"]
    >>> last_etag     = r.headers ["etag"]
    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1", headers = { "If-Modified-Since" : last_modified }))
    { 'headers' :
        { 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' : None
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP.Person/1'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/PAP.Person/1", headers = { "If-None-Match" : last_etag }))
    { 'headers' :
        { 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' : None
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP.Person/1'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '12'
        }
    , 'json' :
        { 'entries' :
            [ 11
            , 12
            ]
        , 'url_template' : '/v1/SRM.Regatta/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM.Regatta'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/SRM.Regatta?verbose"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '12'
        }
    , 'json' :
        { 'entries' :
            [ { 'attributes' :
                  { 'boat_class' :
                      [ 'SRM.Boat_Class'
                      , 7
                      ]
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      [ 'SRM.Regatta_Event'
                      , 10
                      ]
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      [ 'SRM.Handicap'
                      , 9
                      ]
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      [ 'SRM.Regatta_Event'
                      , 10
                      ]
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM.Regatta?verbose'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta_C"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '11'
        }
    , 'json' :
        { 'entries' : [ 11 ]
        , 'url_template' : '/v1/SRM.Regatta_C/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM.Regatta_C'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/SRM.Regatta_H"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '12'
        }
    , 'json' :
        { 'entries' : [ 12 ]
        , 'url_template' : '/v1/SRM.Regatta_H/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM.Regatta_H'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/MOM.Object?verbose"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '10'
        }
    , 'json' :
        { 'entries' :
            [ { 'attributes' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              }
            , { 'attributes' :
                  { 'first_name' : 'Laurens'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'William'
                  , 'title' : ''
                  }
              , 'cid' : 2
              , 'pid' : 2
              , 'type_name' : 'PAP.Person'
              }
            , { 'attributes' :
                  { 'first_name' : 'Clarissa'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : 'Anna'
                  , 'title' : ''
                  }
              , 'cid' : 3
              , 'pid' : 3
              , 'type_name' : 'PAP.Person'
              }
            , { 'attributes' :
                  { 'max_crew' : '1'
                  , 'name' : 'Optimist'
                  }
              , 'cid' : 7
              , 'pid' : 7
              , 'type_name' : 'SRM.Boat_Class'
              }
            , { 'attributes' :
                  { 'name' : 'Yardstick' }
              , 'cid' : 9
              , 'pid' : 9
              , 'type_name' : 'SRM.Handicap'
              }
            , { 'attributes' :
                  { 'date' :
                      [
                        [ 'finish'
                        , '2008/05/01'
                        ]
                      ,
                        [ 'start'
                        , '2008/05/01'
                        ]
                      ]
                  , 'name' : 'Himmelfahrt'
                  }
              , 'cid' : 10
              , 'pid' : 10
              , 'type_name' : 'SRM.Regatta_Event'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM.Object?verbose'
    }

    >>> r = show (requests.get ("http://localhost:9999/v1/MOM.Link?verbose"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '13'
        }
    , 'json' :
        { 'entries' :
            [ { 'attributes' :
                  { 'club' : None
                  , 'left' :
                      [ 'PAP.Person'
                      , 1
                      ]
                  , 'mna_number' : '29676'
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 4
              , 'pid' : 4
              , 'type_name' : 'SRM.Sailor'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' :
                      [ 'PAP.Person'
                      , 2
                      ]
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 5
              , 'pid' : 5
              , 'type_name' : 'SRM.Sailor'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' :
                      [ 'PAP.Person'
                      , 3
                      ]
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 6
              , 'pid' : 6
              , 'type_name' : 'SRM.Sailor'
              }
            , { 'attributes' :
                  { 'left' :
                      [ 'SRM.Boat_Class'
                      , 7
                      ]
                  , 'nation' : 'AUT'
                  , 'sail_number' : '1107'
                  , 'sail_number_x' : ''
                  }
              , 'cid' : 8
              , 'pid' : 8
              , 'type_name' : 'SRM.Boat'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      [ 'SRM.Boat_Class'
                      , 7
                      ]
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      [ 'SRM.Regatta_Event'
                      , 10
                      ]
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      [ 'SRM.Handicap'
                      , 9
                      ]
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      [ 'SRM.Regatta_Event'
                      , 10
                      ]
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              }
            , { 'attributes' :
                  { 'left' :
                      [ 'SRM.Boat'
                      , 8
                      ]
                  , 'right' :
                      [ 'SRM.Regatta_C'
                      , 11
                      ]
                  , 'skipper' :
                      [ 'SRM.Sailor'
                      , 5
                      ]
                  }
              , 'cid' : 13
              , 'pid' : 13
              , 'type_name' : 'SRM.Boat_in_Regatta'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM.Link?verbose'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid/"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '13'
        }
    , 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            , 4
            , 5
            , 6
            , 7
            , 8
            , 9
            , 10
            , 11
            , 12
            , 13
            ]
        , 'url_template' : '/v1/MOM.Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid/1"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '1'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> server.terminate ()

"""

_test_options = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = traverse ("http://localhost:9999/")

    >>> server.terminate ()

"""

_test_post = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (requests.get ("http://localhost:9999/v1/pid?count"))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        , 'x-last-cid' : '13'
        }
    , 'json' :
        { 'count' : 13 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> cargo = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( last_name   = "Dog"
    ...         , first_name  = "Snoopy"
    ...         , middle_name = "the"
    ...         , lifetime    = dict (start = "20001122")
    ...         )
    ...     )
    ... )
    >>> headers = { "Content-Type": "application/json" }
    >>> _ = show (requests.post ("http://localhost:9999/v1/PAP.Person", headers=headers))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request (content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP.Person'
    }

    >>> _ = show (requests.post ("http://localhost:9999/v1/PAP.Person", data=cargo))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request (content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP.Person'
    }

    >>> _ = show (requests.post ("http://localhost:9999/v1/PAP.Person", data=cargo, headers=headers))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'attributes' :
            { 'first_name' : 'Snoopy'
            , 'last_name' : 'Dog'
            , 'lifetime' :
                [
                  [ 'start'
                  , '2000/11/22'
                  ]
                ]
            , 'middle_name' : 'the'
            , 'title' : ''
            }
        , 'cid' : 14
        , 'pid' : 14
        , 'type_name' : 'PAP.Person'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/PAP.Person'
    }

    >>> _ = show (requests.post ("http://localhost:9999/v1/PAP.Person", data=cargo, headers=headers))
    { 'headers' :
        { 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : 'Werkzeug/0.8.3 Python/2.7.3'
        }
    , 'json' :
        { 'error' : "new definition of Person (u'dog', u'snoopy', u'the', u'') clashes with existing Person (u'dog', u'snoopy', u'the', u'')" }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP.Person'
    }

    >>> server.terminate ()

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_cqf      = _test_cqf
        , test_delete   = _test_delete
        , test_get      = _test_get
        #, test_options  = _test_options
        , test_post     = _test_post
        )
    )

if __name__ == "__main__" :
    backend = sos.environ.get \
        ("GTW_test_backends", ("HPS")).split (":") [0].strip ()
    db_url = Scaffold.Backend_Parameters.get (backend, "hps://").strip ("'")
    _run_server (["-db_url", db_url, "-db_name", "test"])
### __END__ GTW.__test__.RST