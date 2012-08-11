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
#    31-Jul-2012 (CT) Add `settimeout` to `run_server`, fix `except` clause
#     2-Aug-2012 (CT) Change sequence of tests in `test_post` (Postgresql
#                     wastes pids for a Name_Clash)
#     2-Aug-2012 (CT) Add `change_query_filters` for entities to `test_cqf`
#     7-Aug-2012 (CT) Add `test_doc`
#     8-Aug-2012 (CT) Add `test_example_*`, continue `test_doc`
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

import _GTW._Werkzeug.Command

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

_Ancestor = GTW.Werkzeug.Command

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

    def create_rst (self, cmd, ** kw) :
        import _GTW._RST._MOM.Doc
        import _GTW._RST._MOM.Scope
        result = GTW.RST.Root \
            ( language          = "de"
            , entries           =
                [ GTW.RST.MOM.Scope        (name = "v1")
                , GTW.RST.MOM.Doc.App_Type (name = "Doc")
                , GTW.RST.Raiser           (name = "RAISE")
                ]
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
        ct    = PAP.Person ("Tanzer", "Christian", raw = True)
        lt    = PAP.Person ("Tanzer", "Laurens", "William", raw = True)
        cat   = PAP.Person ("Tanzer", "Clarissa", "Anna", raw = True)
        ct_s  = SRM.Sailor (ct,  nation = "AUT", mna_number = "29676", raw = True)
        lt_s  = SRM.Sailor (lt,  nation = "AUT", raw = True)
        cat_s = SRM.Sailor (cat, nation = "AUT", raw = True)
        opti  = SRM.Boat_Class ("Optimist", max_crew = "1")
        b     = SRM.Boat ("Optimist", "AUT", "1107", raw = True)
        ys    = SRM.Handicap ("Yardstick", raw = True)
        rev   = SRM.Regatta_Event \
            ("Himmelfahrt", dict (start = "20080501"), raw = True)
        reg   = SRM.Regatta_C (rev, opti)
        reh   = SRM.Regatta_H (rev, ys)
        rev_g = SRM.Regatta_Event \
            ("Guggenberger", dict (start = "20080620", finish = "20080621"), raw = True)
        reg_c = SRM.Regatta_C (rev_g, opti)
        bir   = SRM.Boat_in_Regatta (b, reg,   skipper = lt_s)
        bir_g = SRM.Boat_in_Regatta (b, reg_c, skipper = lt_s)
        scope.commit ()
    # end def fixtures

    @Once_Property
    def src_dir (self) :
        return "/tmp/test"
    # end def src_dir

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

from   posixpath import join as pp_join

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
    tf = tempfile.NamedTemporaryFile (delete = False)
    print ("Using", tf.name, "as stdout/stderr for server process", file=sys.stderr)
    p = subprocess.Popen (cmd, stderr = tf, stdout = tf)
    import socket
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout (1.0)
    i   = 0
    while True :
        try :
            s.connect (("localhost", 9999))
        except socket.error as exc :
            if i < 20 :
                i += 1
                time.sleep (1)
            else :
                break
        else :
            exc = None
            break
    s.close ()
    if exc is not None :
        print  ("Socket connect gave exception:", exc)
        p.kill ()
    return p
# end def run_server

def _normal (k, v) :
    if k in ("date", "last-modified") :
        v = "<datetime instance>"
    elif k in ("etag",) :
        v = "ETag value"
    elif k == "content-length" and int (v) != 0 :
        v = "<length>"
    elif k == "server" :
        v = "<server>"
    return k, v
# end def _normal

def show (r, ** kw) :
    json = r.json if r.content else None
    if json is not None :
        kw ["json"] = json
    elif r.content :
        kw ["content"] = r.content.replace ("\r", "").strip ().split ("\n")
    output = formatted \
        ( dict
            ( status  = r.status_code
            , url     = r.url
            , ** kw
            )
        )
    print (output)
    return r
# end def show

def showf (r, ** kw) :
    return show \
        ( r
        , headers = dict (_normal (k, v) for k, v in r.headers.iteritems ())
        , ** kw
        )
# end def showf

def traverse (url, level = 0, seen = None) :
    if seen is None :
        seen = set ()
    rg    = requests.get     (url)
    ro    = requests.options (url)
    path  = requests.utils.urlparse (url).path or "/"
    if ro.ok :
        allow = ro.headers ["allow"]
        if allow not in seen :
            print (path, ":", allow)
            seen .add (allow)
    else :
        print (path, ":", ro.status_code, ro.content)
    if rg.ok and rg.content and rg.json :
        l = level + 1
        for e in rg.json.get ("entries", ()) :
            traverse (pp_join (url, str (e)), l, seen)
# end def traverse

class Requester (TFL.Meta.Object) :
    """Wrapper for `requests`"""

    class W (TFL.Meta.Object) :

        def __init__ (self, name, prefix) :
            self.method = getattr (requests, name)
            self.prefix = prefix
        # end def __init__

        def __call__ (self, path, * args, ** kw) :
            kw.setdefault ("headers", { "Content-Type": "application/json" })
            url = pp_join (self.prefix, path.lstrip ("/"))
            return self.method (url, * args, ** kw)
        # end def __call__

    # end class W

    def __init__ (self, prefix) :
        self.prefix = prefix
    # end def __init__

    def __getattr__ (self, name) :
        return self.W (name, self.prefix)
    # end def __getattr__

# end class Requester

R = Requester ("http://localhost:9999")

server_args = \
    [ "-UTP=RST"
    , "-auto_reload=no"
    , "-debug=no"
    , "-load_I18N=no"
    , "-log_level=0"
    , "-port=9999"
    ]

### �text� ### The doctest follows::

_test_cqf = r"""
    >>> server = Scaffold (["wsgi"] + server_args + ["-db_url", %(p1)s, "-db_name", %(n1)s or "test"]) # doctest:+ELLIPSIS
    ...
    >>> root   = Scaffold.root
    >>> v1     = root.resource_from_href ("v1")
    >>> pids   = root.resource_from_href ("v1/pid")

    >>> v1
    <Scope v1: /v1>
    >>> pids
    <E_Type MOM-Id_Entity: /v1/MOM-Id_Entity>

    >>> for e in v1.entries :
    ...     print ("%%s\n    %%s" %% (e.name, e.change_query_filters))
    MOM-Id_Entity
        ()
    MOM-Link
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM-Link1
        (Q.type_name.in_ (['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team', 'SWP.Clip_O', 'SWP.Picture'],),)
    MOM-_MOM_Link_n_
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    MOM-Link2
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    MOM-Object
        (Q.type_name.in_ (['PAP.Address', 'PAP.Company', 'PAP.Email', 'PAP.Person', 'PAP.Phone', 'SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event', 'SWP.Gallery', 'SWP.Page'],),)
    PAP-Address
        (Q.type_name == PAP.Address,)
    PAP-Subject
        (Q.type_name.in_ (['PAP.Company', 'PAP.Person'],),)
    PAP-Company
        (Q.type_name == PAP.Company,)
    PAP-Email
        (Q.type_name == PAP.Email,)
    PAP-Phone
        (Q.type_name == PAP.Phone,)
    PAP-Person
        (Q.type_name == PAP.Person,)
    PAP-Subject_has_Property
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone'],),)
    PAP-Subject_has_Address
        (Q.type_name.in_ (['PAP.Company_has_Address', 'PAP.Person_has_Address'],),)
    PAP-Company_has_Address
        (Q.type_name == PAP.Company_has_Address,)
    PAP-Subject_has_Email
        (Q.type_name.in_ (['PAP.Company_has_Email', 'PAP.Person_has_Email'],),)
    PAP-Company_has_Email
        (Q.type_name == PAP.Company_has_Email,)
    PAP-Subject_has_Phone
        (Q.type_name.in_ (['PAP.Company_has_Phone', 'PAP.Person_has_Phone'],),)
    PAP-Company_has_Phone
        (Q.type_name == PAP.Company_has_Phone,)
    PAP-Entity_created_by_Person
        (Q.type_name == PAP.Entity_created_by_Person,)
    PAP-Person_has_Address
        (Q.type_name == PAP.Person_has_Address,)
    PAP-Person_has_Email
        (Q.type_name == PAP.Person_has_Email,)
    PAP-Person_has_Phone
        (Q.type_name == PAP.Person_has_Phone,)
    SRM-Link1
        (Q.type_name.in_ (['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta_C', 'SRM.Regatta_H', 'SRM.Sailor', 'SRM.Team'],),)
    SRM-Link2
        (Q.type_name.in_ (['SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta'],),)
    SRM-Object
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Club', 'SRM.Handicap', 'SRM.Page', 'SRM.Regatta_Event'],),)
    SRM-_Boat_Class_
        (Q.type_name.in_ (['SRM.Boat_Class', 'SRM.Handicap'],),)
    SRM-Boat_Class
        (Q.type_name == SRM.Boat_Class,)
    SRM-Handicap
        (Q.type_name == SRM.Handicap,)
    SRM-Boat
        (Q.type_name == SRM.Boat,)
    SRM-Club
        (Q.type_name == SRM.Club,)
    SRM-Regatta_Event
        (Q.type_name == SRM.Regatta_Event,)
    SWP-Link1
        (Q.type_name.in_ (['SWP.Clip_O', 'SWP.Picture'],),)
    SWP-Object
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP-Object_PN
        (Q.type_name.in_ (['SWP.Gallery', 'SWP.Page'],),)
    SWP-Page
        (Q.type_name == SWP.Page,)
    SWP-Page_Y
        (Q.type_name == SWP.Page_Y,)
    SWP-Clip_O
        (Q.type_name == SWP.Clip_O,)
    SWP-Clip_X
        (Q.type_name == SWP.Clip_X,)
    SWP-Gallery
        (Q.type_name == SWP.Gallery,)
    SWP-Picture
        (Q.type_name == SWP.Picture,)
    SRM-Page
        (Q.type_name == SRM.Page,)
    SRM-Regatta
        (Q.type_name.in_ (['SRM.Regatta_C', 'SRM.Regatta_H'],),)
    SRM-Regatta_C
        (Q.type_name == SRM.Regatta_C,)
    SRM-Regatta_H
        (Q.type_name == SRM.Regatta_H,)
    SRM-Sailor
        (Q.type_name == SRM.Sailor,)
    SRM-Boat_in_Regatta
        (Q.type_name == SRM.Boat_in_Regatta,)
    SRM-Race_Result
        (Q.type_name == SRM.Race_Result,)
    SRM-Team
        (Q.type_name == SRM.Team,)
    SRM-Crew_Member
        (Q.type_name == SRM.Crew_Member,)
    SRM-Team_has_Boat_in_Regatta
        (Q.type_name == SRM.Team_has_Boat_in_Regatta,)

    >>> for e in v1.entries :
    ...     print ("%%s    %%s" %% (e.name, e.attributes))
    MOM-Id_Entity    ()
    MOM-Link    (Left `left`,)
    MOM-Link1    (Left `left`,)
    MOM-_MOM_Link_n_    (Left `left`, Right `right`)
    MOM-Link2    (Left `left`, Right `right`)
    MOM-Object    ()
    PAP-Address    (String `street`, String `zip`, String `city`, String `country`, String `desc`, Position `position`, String `region`)
    PAP-Subject    (Date_Interval `lifetime`,)
    PAP-Company    (String `name`, Date_Interval `lifetime`, String `short_name`)
    PAP-Email    (Email `address`, String `desc`)
    PAP-Phone    (Numeric_String `country_code`, Numeric_String `area_code`, Numeric_String `number`, String `desc`)
    PAP-Person    (String `last_name`, String `first_name`, String `middle_name`, String `title`, Date_Interval `lifetime`, String `salutation`, Sex `sex`)
    PAP-Subject_has_Property    (Subject `left`, Right `right`, String `desc`)
    PAP-Subject_has_Address    (Subject `left`, Address `right`, String `desc`)
    PAP-Company_has_Address    (Company `left`, Address `right`, String `desc`)
    PAP-Subject_has_Email    (Subject `left`, Email `right`, String `desc`)
    PAP-Company_has_Email    (Company `left`, Email `right`, String `desc`)
    PAP-Subject_has_Phone    (Subject `left`, Phone `right`, String `desc`)
    PAP-Company_has_Phone    (Company `left`, Phone `right`, String `desc`)
    PAP-Entity_created_by_Person    (Id_Entity `left`, Person `right`)
    PAP-Person_has_Address    (Person `left`, Address `right`, String `desc`)
    PAP-Person_has_Email    (Person `left`, Email `right`, String `desc`)
    PAP-Person_has_Phone    (Person `left`, Phone `right`, Numeric_String `extension`, String `desc`)
    SRM-Link1    (Left `left`,)
    SRM-Link2    (Left `left`, Right `right`)
    SRM-Object    ()
    SRM-_Boat_Class_    (String `name`,)
    SRM-Boat_Class    (String `name`, Int `max_crew`, Float `beam`, Float `loa`, Float `sail_area`)
    SRM-Handicap    (String `name`,)
    SRM-Boat    (Boat_Class `left`, Nation `nation`, Int `sail_number`, String `sail_number_x`, String `name`)
    SRM-Club    (String `name`, String `long_name`)
    SRM-Regatta_Event    (String `name`, Date_Interval `date`, Entity `club`, String `desc`, Boolean `is_cancelled`)
    SWP-Link1    (Left `left`,)
    SWP-Object    ()
    SWP-Object_PN    (Date-Slug `perma_name`, Date_Interval `date`, String `short_title`, String `title`)
    SWP-Page    (Date-Slug `perma_name`, Text `text`, Date_Interval `date`, String `short_title`, String `title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`)
    SWP-Page_Y    (Date-Slug `perma_name`, Int `year`, Text `text`, Date_Interval `date`, String `short_title`, String `title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`)
    SWP-Clip_O    (Object_PN `left`, Date_Interval `date_x`, Text `abstract`, Int `prio`)
    SWP-Clip_X    (Date-Slug `perma_name`, Text `text`, Date_Interval `date`, String `short_title`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`, Url `link_to`, String `title`)
    SWP-Gallery    (Date-Slug `perma_name`, Date_Interval `date`, String `short_title`, String `title`, Directory `directory`)
    SWP-Picture    (Gallery `left`, Int `number`, Picture `photo`, Thumbnail `thumb`)
    SRM-Page    (Date-Slug `perma_name`, Entity `event`, Text `text`, Date_Interval `date`, Format `format`, String `head_line`, Boolean `hidden`, Int `prio`, String `desc`)
    SRM-Regatta    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`)
    SRM-Regatta_C    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`, Boolean `is_team_race`)
    SRM-Regatta_H    (Regatta_Event `left`, Entity `boat_class`, Int `discards`, Boolean `is_cancelled`, String `kind`, Int `races`, Regatta_Result `result`)
    SRM-Sailor    (Person `left`, Nation `nation`, Int `mna_number`, Entity `club`)
    SRM-Boat_in_Regatta    (Boat `left`, Regatta `right`, Entity `skipper`, Int `place`, Int `points`)
    SRM-Race_Result    (Boat_in_Regatta `left`, Int `race`, Int `points`, String `status`, Boolean `discarded`)
    SRM-Team    (Regatta_C `left`, String `name`, Entity `club`, String `desc`, Entity `leader`, Int `place`)
    SRM-Crew_Member    (Boat_in_Regatta `left`, Sailor `right`, Int `key`, String `role`)
    SRM-Team_has_Boat_in_Regatta    (Team `left`, Boat_in_Regatta `right`)

    >>> print (root.href_pat_frag)
    v1(?:/(?:SWP\-Picture|SWP\-Page\_Y|SWP\-Page|SWP\-Object\_PN|SWP\-Object|SWP\-Link1|SWP\-Gallery|SWP\-Clip\_X|SWP\-Clip\_O|SRM\-\_Boat\_Class\_|SRM\-Team\_has\_Boat\_in\_Regatta|SRM\-Team|SRM\-Sailor|SRM\-Regatta\_H|SRM\-Regatta\_Event|SRM\-Regatta\_C|SRM\-Regatta|SRM\-Race\_Result|SRM\-Page|SRM\-Object|SRM\-Link2|SRM\-Link1|SRM\-Handicap|SRM\-Crew\_Member|SRM\-Club|SRM\-Boat\_in\_Regatta|SRM\-Boat\_Class|SRM\-Boat|PAP\-Subject\_has\_Property|PAP\-Subject\_has\_Phone|PAP\-Subject\_has\_Email|PAP\-Subject\_has\_Address|PAP\-Subject|PAP\-Phone|PAP\-Person\_has\_Phone|PAP\-Person\_has\_Email|PAP\-Person\_has\_Address|PAP\-Person|PAP\-Entity\_created\_by\_Person|PAP\-Email|PAP\-Company\_has\_Phone|PAP\-Company\_has\_Email|PAP\-Company\_has\_Address|PAP\-Company|PAP\-Address|MOM\-\_MOM\_Link\_n\_|MOM\-Object|MOM\-Link2|MOM\-Link1|MOM\-Link|MOM\-Id\_Entity))?|Doc

    >>> for o in sorted (pids.objects, key = Q.pid) :
    ...     e = pids._new_entry (o.pid)
    ...     print ("%%s %%r\n    %%s" %% (e.E_Type.type_name, o.ui_display, e.change_query_filters))
    PAP.Person u'Tanzer Christian'
        (Q.pid == 1,)
    PAP.Person u'Tanzer Laurens William'
        (Q.pid == 2,)
    PAP.Person u'Tanzer Clarissa Anna'
        (Q.pid == 3,)
    SRM.Sailor u'Tanzer Christian, AUT, 29676'
        (Q.pid.in_ ((4, 1),),)
    SRM.Sailor u'Tanzer Laurens William, AUT'
        (Q.pid.in_ ((5, 2),),)
    SRM.Sailor u'Tanzer Clarissa Anna, AUT'
        (Q.pid.in_ ((6, 3),),)
    SRM.Boat_Class u'Optimist'
        (Q.pid == 7,)
    SRM.Boat u'Optimist, AUT 1107'
        (Q.pid.in_ ((8, 7),),)
    SRM.Handicap u'Yardstick'
        (Q.pid == 9,)
    SRM.Regatta_Event u'Himmelfahrt 2008/05/01'
        (Q.pid == 10,)
    SRM.Regatta_C u'Himmelfahrt 2008/05/01, Optimist'
        (Q.pid.in_ ((11, 10, 7),),)
    SRM.Regatta_H u'Himmelfahrt 2008/05/01, Yardstick'
        (Q.pid.in_ ((12, 10, 9),),)
    SRM.Regatta_Event u'Guggenberger 2008/06/20 - 2008/06/21'
        (Q.pid == 13,)
    SRM.Regatta_C u'Guggenberger 2008/06/20 - 2008/06/21, Optimist'
        (Q.pid.in_ ((14, 13, 7),),)
    SRM.Boat_in_Regatta u'Optimist, AUT 1107, Himmelfahrt 2008/05/01, Optimist'
        (Q.pid.in_ ((15, 8, 11, 5),),)
    SRM.Boat_in_Regatta u'Optimist, AUT 1107, Guggenberger 2008/06/20 - 2008/06/21, Optimist'
        (Q.pid.in_ ((16, 8, 14, 5),),)

"""

_test_delete = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid/")) ### 1
    { 'json' :
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
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (R.get ("/v1/pid/1"))  ### 2
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.delete ("/v1/pid/1")) ### 3
    { 'json' :
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
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 2))) ### 4
    { 'json' :
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
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=2'
    }

    >>> _ = show (R.get ("/v1/pid?count")) ### 5
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 1))) ### 6
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'status' : 'Object with pid 1 successfully deleted'
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (R.get ("/v1/pid?count")) ### 7
    { 'json' :
        { 'count' : 14 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.delete ("/v1/pid/1", params = dict (cid = 1))) ### 8
    { 'json' :
        { 'description' : 'Gone' }
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1?cid=1'
    }

    >>> _ = show (R.get ("/v1/pid/1")) ### 9
    { 'json' :
        { 'description' : 'Gone' }
    , 'status' : 410
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.get ("/v1/pid")) ### 10
    { 'json' :
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
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid'
    }

    >>> server.terminate ()

"""

_test_doc = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/Doc"))
    { 'json' :
        { 'entries' :
            [ 'PAP-Address'
            , 'PAP-Company'
            , 'PAP-Email'
            , 'PAP-Phone'
            , 'PAP-Person'
            , 'PAP-Company_has_Address'
            , 'PAP-Company_has_Email'
            , 'PAP-Company_has_Phone'
            , 'PAP-Entity_created_by_Person'
            , 'PAP-Person_has_Address'
            , 'PAP-Person_has_Email'
            , 'PAP-Person_has_Phone'
            , 'SRM-_Boat_Class_'
            , 'SRM-Boat_Class'
            , 'SRM-Handicap'
            , 'SRM-Boat'
            , 'SRM-Club'
            , 'SRM-Regatta_Event'
            , 'SWP-Page'
            , 'SWP-Page_Y'
            , 'SWP-Clip_O'
            , 'SWP-Clip_X'
            , 'SWP-Gallery'
            , 'SWP-Picture'
            , 'SRM-Page'
            , 'SRM-Regatta'
            , 'SRM-Regatta_C'
            , 'SRM-Regatta_H'
            , 'SRM-Sailor'
            , 'SRM-Boat_in_Regatta'
            , 'SRM-Race_Result'
            , 'SRM-Team'
            , 'SRM-Crew_Member'
            , 'SRM-Team_has_Boat_in_Regatta'
            ]
        , 'url_template' : '/Doc/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc'
    }

    >>> _ = show (R.get ("/Doc/SRM-Boat_in_Regatta"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Boat racing in a regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Boat'
              , 'role_name' : 'boat'
              , 'type' : 'Boat'
              , 'type_name' : 'SRM.Boat'
              , 'ui_name' : 'Boat'
              , 'url' : '/Doc/SRM-Boat'
              }
            , { 'default_value' : ''
              , 'description' : 'Regatta a boat races in.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'right'
              , 'p_type' : 'Regatta'
              , 'role_name' : 'regatta'
              , 'type' : 'Regatta'
              , 'type_name' : 'SRM.Regatta'
              , 'ui_name' : 'Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            , { 'default_value' : ''
              , 'description' : 'Skipper of boat.'
              , 'is_required' : True
              , 'kind' : 'required'
              , 'name' : 'skipper'
              , 'p_type' : 'Sailor'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Sailor'
              , 'ui_name' : 'Skipper'
              , 'url' : '/Doc/SRM-Sailor'
              }
            , { 'default_value' : ''
              , 'description' : 'Place of boat in this regatta.'
              , 'example' : 2
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'place'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Place'
              }
            , { 'default_value' : ''
              , 'description' : 'Total points of boat in this regatta.'
              , 'example' : 25
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'points'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Points'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'PAP.Entity_created_by_Person'
              , 'url' : '/Doc/PAP-Entity_created_by_Person'
              }
            , { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Crew_Member'
              , 'url' : '/Doc/SRM-Crew_Member'
              }
            , { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Race_Result'
              , 'url' : '/Doc/SRM-Race_Result'
              }
            , { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Team_has_Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Team_has_Boat_in_Regatta'
              }
            ]
        , 'description' : 'Boat racing in a regatta.'
        , 'type_name' : 'SRM.Boat_in_Regatta'
        , 'ui_name' : 'SRM.Boat_in_Regatta'
        , 'url' : '/Doc/SRM-Boat_in_Regatta'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Boat_in_Regatta'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Class of boats sailing in this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : '_Boat_Class_'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM._Boat_Class_'
              , 'ui_name' : 'Boat class'
              , 'url' : '/Doc/SRM-_Boat_Class_'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            ]
        , 'children' :
            [ { 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/Doc/SRM-Regatta_C'
              }
            , { 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/Doc/SRM-Regatta_H'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'PAP.Entity_created_by_Person'
              , 'url' : '/Doc/PAP-Entity_created_by_Person'
              }
            , { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            ]
        , 'description' : 'Sailing regatta for one class or handicap.'
        , 'type_name' : 'SRM.Regatta'
        , 'ui_name' : 'SRM.Regatta'
        , 'url' : '/Doc/SRM-Regatta'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta_C"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Class of boats sailing in this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : 'Boat_Class'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Boat_Class'
              , 'ui_name' : 'Boat class'
              , 'url' : '/Doc/SRM-Boat_Class'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            , { 'default_value' : 'no'
              , 'description' : 'Boolean attribute.'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_team_race'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is team race'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'PAP.Entity_created_by_Person'
              , 'url' : '/Doc/PAP-Entity_created_by_Person'
              }
            , { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            , { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'SRM.Team'
              , 'url' : '/Doc/SRM-Team'
              }
            ]
        , 'description' : 'Regatta for a single class of sail boats.'
        , 'parents' :
            [ { 'type_name' : 'SRM.Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            ]
        , 'relevant_root' :
            { 'type_name' : 'SRM.Regatta'
            , 'url' : '/Doc/SRM-Regatta'
            }
        , 'type_name' : 'SRM.Regatta_C'
        , 'ui_name' : 'SRM.Regatta_C'
        , 'url' : '/Doc/SRM-Regatta_C'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta_C'
    }

    >>> _ = show (R.get ("/Doc/SRM-Regatta_H"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : 'Regatta event to which this regatta belongs.'
              , 'is_changeable' : False
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Regatta_Event'
              , 'role_name' : 'event'
              , 'type' : 'Regatta_Event'
              , 'type_name' : 'SRM.Regatta_Event'
              , 'ui_name' : 'Event'
              , 'url' : '/Doc/SRM-Regatta_Event'
              }
            , { 'default_value' : ''
              , 'description' : 'Name of handicap system used for this regatta.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'boat_class'
              , 'p_type' : 'Handicap'
              , 'type' : 'Entity'
              , 'type_name' : 'SRM.Handicap'
              , 'ui_name' : 'Handicap'
              , 'url' : '/Doc/SRM-Handicap'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of discardable races in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'discards'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Discards'
              }
            , { 'default_value' : ''
              , 'description' : 'Indicates that the regatta is cancelled'
              , 'example' : 'no'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'is_cancelled'
              , 'p_type' : 'bool'
              , 'syntax' : 'The following string values are accepted as valid Boolean values: no, yes'
              , 'type' : 'Boolean'
              , 'ui_name' : 'Is cancelled'
              }
            , { 'default_value' : ''
              , 'description' : 'Kind of regatta.'
              , 'example' : 'One race, one beer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'kind'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Kind'
              }
            , { 'default_value' : '0'
              , 'description' : 'Number of races sailed in regatta'
              , 'example' : '42'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'races'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Races'
              }
            , { 'attributes' :
                  [ { 'default_value' : ''
                    , 'description' : 'Date of regatta result.'
                    , 'example' : '1979/08/18'
                    , 'is_required' : False
                    , 'kind' : 'necessary'
                    , 'name' : 'date'
                    , 'p_type' : 'datetime'
                    , 'type' : 'Date-Time'
                    , 'ui_name' : 'Date'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Name of software used for managing the regatta.'
                    , 'example' : 'Blowing Bits Inc.'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'software'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Software'
                    }
                  , { 'default_value' : ''
                    , 'description' : 'Status of result (e.g., `preliminary` or `final`).'
                    , 'example' : 'Final'
                    , 'is_required' : False
                    , 'kind' : 'optional'
                    , 'max_length' : 64
                    , 'name' : 'status'
                    , 'p_type' : 'unicode'
                    , 'type' : 'String'
                    , 'ui_name' : 'Status'
                    }
                  ]
              , 'default_value' : ''
              , 'description' : 'Information about result.'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'result'
              , 'p_type' : 'Regatta_Result'
              , 'type' : 'Regatta_Result'
              , 'type_name' : 'SRM.Regatta_Result'
              , 'ui_name' : 'Result'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'PAP.Entity_created_by_Person'
              , 'url' : '/Doc/PAP-Entity_created_by_Person'
              }
            , { 'attributes' :
    [ 'right' ]
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            ]
        , 'description' : 'Regatta for boats in a handicap system.'
        , 'parents' :
            [ { 'type_name' : 'SRM.Regatta'
              , 'url' : '/Doc/SRM-Regatta'
              }
            ]
        , 'relevant_root' :
            { 'type_name' : 'SRM.Regatta'
            , 'url' : '/Doc/SRM-Regatta'
            }
        , 'type_name' : 'SRM.Regatta_H'
        , 'ui_name' : 'SRM.Regatta_H'
        , 'url' : '/Doc/SRM-Regatta_H'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Regatta_H'
    }

    >>> _ = show (R.get ("/Doc/SRM-Crew_Member"))
    { 'json' :
        { 'attributes' :
            [ { 'default_value' : ''
              , 'description' : '`Boat_in_Regatta` the crew member sails on.'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'left'
              , 'p_type' : 'Boat_in_Regatta'
              , 'role_name' : 'boat_in_regatta'
              , 'type' : 'Boat_in_Regatta'
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'ui_name' : 'Boat in regatta'
              , 'url' : '/Doc/SRM-Boat_in_Regatta'
              }
            , { 'default_value' : ''
              , 'description' : 'Person which sails as crew member on `boat_in_regatta`'
              , 'is_required' : True
              , 'kind' : 'primary'
              , 'name' : 'right'
              , 'p_type' : 'Sailor'
              , 'role_name' : 'sailor'
              , 'type' : 'Sailor'
              , 'type_name' : 'SRM.Sailor'
              , 'ui_name' : 'Sailor'
              , 'url' : '/Doc/SRM-Sailor'
              }
            , { 'default_value' : '0'
              , 'description' : 'The crew members of a boat will be sorted by `key`, if\ndefined, by order of creation otherwise.'
              , 'example' : 7
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'name' : 'key'
              , 'p_type' : 'int'
              , 'type' : 'Int'
              , 'ui_name' : 'Key'
              }
            , { 'default_value' : ''
              , 'description' : 'Role of crew member.'
              , 'example' : 'trimmer'
              , 'is_required' : False
              , 'kind' : 'optional'
              , 'max_length' : 32
              , 'name' : 'role'
              , 'p_type' : 'unicode'
              , 'type' : 'String'
              , 'ui_name' : 'Role'
              }
            ]
        , 'cross_references' :
            [ { 'attributes' :
    [ 'left' ]
              , 'type_name' : 'PAP.Entity_created_by_Person'
              , 'url' : '/Doc/PAP-Entity_created_by_Person'
              }
            ]
        , 'description' : 'Crew member of a `Boat_in_Regatta`.'
        , 'type_name' : 'SRM.Crew_Member'
        , 'ui_name' : 'SRM.Crew_Member'
        , 'url' : '/Doc/SRM-Crew_Member'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/Doc/SRM-Crew_Member'
    }

    >>> server.terminate ()

"""

_test_example_1 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print ("Count before loop:", scope.MOM.Id_Entity.count)
    Count before loop: 16

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), 'PAP.Company_has_Phone')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Entity_created_by_Person : ------
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', u'99', 'PAP.Person_has_Phone')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : ((u'', u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ------
    SRM.Regatta_C : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ------
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Team : ------
    SRM.Team_has_Boat_in_Regatta : ------
    SWP.Clip_O : ------
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> print ("Count after loop:", scope.MOM.Id_Entity.count)
    Count after loop: 16

    >>> scope.destroy ()

"""

_test_example_2 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) : ### nummero 2
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), 'PAP.Company_has_Phone')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Entity_created_by_Person : ------
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', u'99', 'PAP.Person_has_Phone')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : ((u'', u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ------
    SRM.Regatta_C : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ------
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Team : ------
    SRM.Team_has_Boat_in_Regatta : ------
    SWP.Clip_O : ------
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> scope.destroy ()

"""

_test_example_3 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np, reverse = True) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Clip_O : ------
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SRM.Team : (u'', u'foo', 'SRM.Team')
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Regatta_H : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_C : ------
    SRM.Race_Result : ------
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Crew_Member : ------
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Boat_in_Regatta : ------
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat : (u'', u'AUT', u'2827', u'X', 'SRM.Boat')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Entity_created_by_Person : ------
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Phone')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Email')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')

    >>> scope.destroy ()

"""

_test_example_4 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print ("Count before loop:", scope.MOM.Id_Entity.count)
    Count before loop: 16

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), 'PAP.Company_has_Phone')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Entity_created_by_Person : ------
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', u'99', 'PAP.Person_has_Phone')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : ((u'', u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ------
    SRM.Regatta_C : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ------
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Team : ------
    SRM.Team_has_Boat_in_Regatta : ------
    SWP.Clip_O : ------
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> scope.destroy ()

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np) : ### nummero 2
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Company_has_Address')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Company_has_Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), (u'43', u'1', u'234567', 'PAP.Phone'), 'PAP.Company_has_Phone')
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Entity_created_by_Person : ------
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Address')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', 'PAP.Person_has_Email')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), u'', u'99', 'PAP.Person_has_Phone')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    SRM.Boat : ((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat')
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat_in_Regatta : ((u'', u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Crew_Member : ------
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Race_Result : ------
    SRM.Regatta_C : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_H : ------
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Team : ------
    SRM.Team_has_Boat_in_Regatta : ------
    SWP.Clip_O : ------
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')

    >>> scope.destroy ()

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> for tn in sorted (scope.MOM.Id_Entity.children_np, reverse = True) :
    ...     ETM = scope [tn]
    ...     exa = ETM.example ()
    ...     print (tn, ":", exa.epk_raw if exa is not None else "------")
    ...     scope.rollback ()
    SWP.Picture : ((u'20101010_000042_137', 'SWP.Gallery'), u'42', 'SWP.Picture')
    SWP.Page : (u'20101010_000042_137', 'SWP.Page')
    SWP.Gallery : (u'20101010_000042_137', 'SWP.Gallery')
    SWP.Clip_O : ------
    SRM.Team_has_Boat_in_Regatta : ((((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), u'foo', 'SRM.Team'), (((u'Laser', 'SRM.Boat_Class'), u'AUT', u'2827', u'X', 'SRM.Boat'), ((u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), (u'Laser', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), 'SRM.Team_has_Boat_in_Regatta')
    SRM.Team : (u'', u'foo', 'SRM.Team')
    SRM.Sailor : (u'', u'AUT', u'499999.5', u'', 'SRM.Sailor')
    SRM.Regatta_H : ------
    SRM.Regatta_Event : (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event')
    SRM.Regatta_C : ------
    SRM.Race_Result : ------
    SRM.Page : (u'20101010_000042_137', (u'Fastnet Race', (('finish', u'2038/01/19'), ('start', u'1970/01/01')), 'SRM.Regatta_Event'), 'SRM.Page')
    SRM.Handicap : (u'IRC', 'SRM.Handicap')
    SRM.Crew_Member : ------
    SRM.Club : (u'RORC', 'SRM.Club')
    SRM.Boat_in_Regatta : ------
    SRM.Boat_Class : (u'Laser', 'SRM.Boat_Class')
    SRM.Boat : (u'', u'AUT', u'2827', u'X', 'SRM.Boat')
    PAP.Phone : (u'43', u'1', u'234567', 'PAP.Phone')
    PAP.Person_has_Phone : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'43', u'1', u'234567', 'PAP.Phone'), u'99', 'PAP.Person_has_Phone')
    PAP.Person_has_Email : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'john.doe@example.com', 'PAP.Email'), 'PAP.Person_has_Email')
    PAP.Person_has_Address : ((u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person'), (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address'), 'PAP.Person_has_Address')
    PAP.Person : (u'Doe', u'John', u'F.', u'Dr.', 'PAP.Person')
    PAP.Entity_created_by_Person : ------
    PAP.Email : (u'john.doe@example.com', 'PAP.Email')
    PAP.Company_has_Phone : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Phone')
    PAP.Company_has_Email : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Email')
    PAP.Company_has_Address : ((u'John Doe, Inc.', 'PAP.Company'), u'', 'PAP.Company_has_Address')
    PAP.Company : (u'John Doe, Inc.', 'PAP.Company')
    PAP.Address : (u'Mystery Lane 42', u'9876', u'Middletown', u'Land of the Brave', 'PAP.Address')

    >>> scope.destroy ()

"""

_test_get = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> r = showf (R.options (""))
    { 'headers' :
        { 'allow' : 'GET, HEAD, OPTIONS'
        , 'content-length' : '0'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'server' : '<server>'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = showf (R.head (""))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'content-length' : '0'
        , 'content-type' : 'text/plain; charset=utf-8'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'server' : '<server>'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (R.get (""))
    { 'json' :
        { 'entries' :
            [ 'v1'
            , 'Doc'
            , 'RAISE'
            ]
        , 'url_template' : '/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/'
    }

    >>> r = show (R.get ("?verbose"))
    { 'json' :
        { 'entries' :
            [ '/v1'
            , '/Doc'
            , '/RAISE'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/?verbose'
    }

    >>> r = show (R.get ("/v0"))
    { 'json' :
        { 'description' : 'Not found' }
    , 'status' : 404
    , 'url' : 'http://localhost:9999/v0'
    }

    >>> r = show (R.get ("/v1"))
    { 'json' :
        { 'entries' :
            [ 'MOM-Id_Entity'
            , 'MOM-Link'
            , 'MOM-Link1'
            , 'MOM-_MOM_Link_n_'
            , 'MOM-Link2'
            , 'MOM-Object'
            , 'PAP-Address'
            , 'PAP-Subject'
            , 'PAP-Company'
            , 'PAP-Email'
            , 'PAP-Phone'
            , 'PAP-Person'
            , 'PAP-Subject_has_Property'
            , 'PAP-Subject_has_Address'
            , 'PAP-Company_has_Address'
            , 'PAP-Subject_has_Email'
            , 'PAP-Company_has_Email'
            , 'PAP-Subject_has_Phone'
            , 'PAP-Company_has_Phone'
            , 'PAP-Entity_created_by_Person'
            , 'PAP-Person_has_Address'
            , 'PAP-Person_has_Email'
            , 'PAP-Person_has_Phone'
            , 'SRM-Link1'
            , 'SRM-Link2'
            , 'SRM-Object'
            , 'SRM-_Boat_Class_'
            , 'SRM-Boat_Class'
            , 'SRM-Handicap'
            , 'SRM-Boat'
            , 'SRM-Club'
            , 'SRM-Regatta_Event'
            , 'SWP-Link1'
            , 'SWP-Object'
            , 'SWP-Object_PN'
            , 'SWP-Page'
            , 'SWP-Page_Y'
            , 'SWP-Clip_O'
            , 'SWP-Clip_X'
            , 'SWP-Gallery'
            , 'SWP-Picture'
            , 'SRM-Page'
            , 'SRM-Regatta'
            , 'SRM-Regatta_C'
            , 'SRM-Regatta_H'
            , 'SRM-Sailor'
            , 'SRM-Boat_in_Regatta'
            , 'SRM-Race_Result'
            , 'SRM-Team'
            , 'SRM-Crew_Member'
            , 'SRM-Team_has_Boat_in_Regatta'
            ]
        , 'url_template' : '/v1/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1'
    }

    >>> r = show (R.get ("/v1?verbose"))
    { 'json' :
        { 'entries' :
            [ '/v1/MOM-Id_Entity'
            , '/v1/MOM-Link'
            , '/v1/MOM-Link1'
            , '/v1/MOM-_MOM_Link_n_'
            , '/v1/MOM-Link2'
            , '/v1/MOM-Object'
            , '/v1/PAP-Address'
            , '/v1/PAP-Subject'
            , '/v1/PAP-Company'
            , '/v1/PAP-Email'
            , '/v1/PAP-Phone'
            , '/v1/PAP-Person'
            , '/v1/PAP-Subject_has_Property'
            , '/v1/PAP-Subject_has_Address'
            , '/v1/PAP-Company_has_Address'
            , '/v1/PAP-Subject_has_Email'
            , '/v1/PAP-Company_has_Email'
            , '/v1/PAP-Subject_has_Phone'
            , '/v1/PAP-Company_has_Phone'
            , '/v1/PAP-Entity_created_by_Person'
            , '/v1/PAP-Person_has_Address'
            , '/v1/PAP-Person_has_Email'
            , '/v1/PAP-Person_has_Phone'
            , '/v1/SRM-Link1'
            , '/v1/SRM-Link2'
            , '/v1/SRM-Object'
            , '/v1/SRM-_Boat_Class_'
            , '/v1/SRM-Boat_Class'
            , '/v1/SRM-Handicap'
            , '/v1/SRM-Boat'
            , '/v1/SRM-Club'
            , '/v1/SRM-Regatta_Event'
            , '/v1/SWP-Link1'
            , '/v1/SWP-Object'
            , '/v1/SWP-Object_PN'
            , '/v1/SWP-Page'
            , '/v1/SWP-Page_Y'
            , '/v1/SWP-Clip_O'
            , '/v1/SWP-Clip_X'
            , '/v1/SWP-Gallery'
            , '/v1/SWP-Picture'
            , '/v1/SRM-Page'
            , '/v1/SRM-Regatta'
            , '/v1/SRM-Regatta_C'
            , '/v1/SRM-Regatta_H'
            , '/v1/SRM-Sailor'
            , '/v1/SRM-Boat_in_Regatta'
            , '/v1/SRM-Race_Result'
            , '/v1/SRM-Team'
            , '/v1/SRM-Crew_Member'
            , '/v1/SRM-Team_has_Boat_in_Regatta'
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1?verbose'
    }

    >>> rp = show (R.get ("/v1/PAP-Person"))
    { 'json' :
        { 'entries' :
            [ 1
            , 2
            , 3
            ]
        , 'url_template' : '/v1/PAP-Person/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.get ("/v1/PAP-Person?verbose"))
    { 'json' :
        { 'attribute_names' :
            [ 'last_name'
            , 'first_name'
            , 'middle_name'
            , 'title'
            , 'lifetime'
            , 'salutation'
            , 'sex'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/PAP-Person/1'
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
              , 'url' : '/v1/PAP-Person/2'
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
              , 'url' : '/v1/PAP-Person/3'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person?verbose'
    }

    >>> _ = show (R.get ("/v1/PAP-Person.csv?verbose"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime,salutation,sex'
        , 'Tanzer,Christian,,,,,'
        , 'Tanzer,Laurens,William,,,,'
        , 'Tanzer,Clarissa,Anna,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?verbose'
    }
    >>> _ = show (R.get ("/v1/PAP-Person.csv"))
    { 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv'
    }

    >>> for pid in rp.json ["entries"] :
    ...     _ = show (requests.get (pp_join (rp.url, str (pid))))
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Laurens'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'William'
            , 'title' : ''
            }
        , 'cid' : 2
        , 'pid' : 2
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/2'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/2'
    }
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Clarissa'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : 'Anna'
            , 'title' : ''
            }
        , 'cid' : 3
        , 'pid' : 3
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/3'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/3'
    }

    >>> r = show (R.head ("/v1/PAP-Person/1"))
    { 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = showf (R.get ("/v1/PAP-Person/1"))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'content-length' : '<length>'
        , 'content-type' : 'application/json'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'last-modified' : '<datetime instance>'
        , 'server' : '<server>'
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
        , 'url' : '/v1/PAP-Person/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> last_modified = r.headers ["last-modified"]
    >>> last_etag     = r.headers ["etag"]
    >>> r = showf (R.get ("/v1/PAP-Person/1", headers = { "If-Modified-Since" : last_modified }))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'server' : '<server>'
        , 'x-last-cid' : '1'
        }
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = showf (R.get ("/v1/PAP-Person/1", headers = { "If-None-Match" : last_etag }))
    { 'headers' :
        { 'cache-control' : 'no-cache'
        , 'connection' : 'close'
        , 'date' : '<datetime instance>'
        , 'etag' : 'ETag value'
        , 'server' : '<server>'
        , 'x-last-cid' : '1'
        }
    , 'status' : 304
    , 'url' : 'http://localhost:9999/v1/PAP-Person/1'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta"))
    { 'json' :
        { 'entries' :
            [ 11
            , 12
            , 14
            ]
        , 'url_template' : '/v1/SRM-Regatta/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose"))
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'boat_class'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'boat_class' : 7
                  , 'is_cancelled' : 'no'
                  , 'left' : 10
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes' :
                  { 'boat_class' : 9
                  , 'is_cancelled' : 'no'
                  , 'left' : 10
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes' :
                  { 'boat_class' : 7
                  , 'is_cancelled' : 'no'
                  , 'left' : 13
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta.csv?verbose"))
    { 'content' :
        [ 'left,boat_class,discards,is_cancelled,kind,races,result'
        , '10,7,,no,,,'
        , '10,9,,no,,,'
        , '13,7,,no,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta.csv?verbose'
    }

    >>> _ = show (R.get ("/v1/SRM-Regatta?verbose&closure"))
    { 'json' :
        { 'attribute_names' :
            [ 'left'
            , 'boat_class'
            , 'discards'
            , 'is_cancelled'
            , 'kind'
            , 'races'
            , 'result'
            ]
        , 'entries' :
            [ { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Optimist' }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
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
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/11'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
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
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/SRM-Regatta/12'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Optimist' }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
                          { 'date' :
                              [
                                [ 'finish'
                                , '2008/06/21'
                                ]
                              ,
                                [ 'start'
                                , '2008/06/20'
                                ]
                              ]
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/SRM-Regatta/14'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta?verbose&closure'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta_C"))
    { 'json' :
        { 'entries' :
            [ 11
            , 14
            ]
        , 'url_template' : '/v1/SRM-Regatta_C/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta_C'
    }

    >>> r = show (R.get ("/v1/SRM-Regatta_H"))
    { 'json' :
        { 'entries' : [ 12 ]
        , 'url_template' : '/v1/SRM-Regatta_H/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Regatta_H'
    }

    >>> r = show (R.get ("/v1/MOM-Object?verbose"))
    { 'json' :
        { 'attribute_names' :
            []
        , 'entries' :
            [ { 'attributes' :
                  { 'first_name' : 'Christian'
                  , 'last_name' : 'Tanzer'
                  , 'middle_name' : ''
                  , 'title' : ''
                  }
              , 'cid' : 1
              , 'pid' : 1
              , 'type_name' : 'PAP.Person'
              , 'url' : '/v1/MOM-Object/1'
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
              , 'url' : '/v1/MOM-Object/2'
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
              , 'url' : '/v1/MOM-Object/3'
              }
            , { 'attributes' :
                  { 'max_crew' : '1'
                  , 'name' : 'Optimist'
                  }
              , 'cid' : 7
              , 'pid' : 7
              , 'type_name' : 'SRM.Boat_Class'
              , 'url' : '/v1/MOM-Object/7'
              }
            , { 'attributes' :
                  { 'name' : 'Yardstick' }
              , 'cid' : 9
              , 'pid' : 9
              , 'type_name' : 'SRM.Handicap'
              , 'url' : '/v1/MOM-Object/9'
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
              , 'url' : '/v1/MOM-Object/10'
              }
            , { 'attributes' :
                  { 'date' :
                      [
                        [ 'finish'
                        , '2008/06/21'
                        ]
                      ,
                        [ 'start'
                        , '2008/06/20'
                        ]
                      ]
                  , 'name' : 'Guggenberger'
                  }
              , 'cid' : 13
              , 'pid' : 13
              , 'type_name' : 'SRM.Regatta_Event'
              , 'url' : '/v1/MOM-Object/13'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Object?verbose'
    }

    >>> r = show (R.get ("/v1/MOM-Link?verbose"))
    { 'json' :
        { 'attribute_names' :
    [ 'left' ]
        , 'entries' :
            [ { 'attributes' :
                  { 'club' : None
                  , 'left' : 1
                  , 'mna_number' : '29676'
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 4
              , 'pid' : 4
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/4'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' : 2
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 5
              , 'pid' : 5
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/5'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' : 3
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 6
              , 'pid' : 6
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/6'
              }
            , { 'attributes' :
                  { 'left' : 7
                  , 'nation' : 'AUT'
                  , 'sail_number' : '1107'
                  , 'sail_number_x' : ''
                  }
              , 'cid' : 8
              , 'pid' : 8
              , 'type_name' : 'SRM.Boat'
              , 'url' : '/v1/MOM-Link/8'
              }
            , { 'attributes' :
                  { 'boat_class' : 7
                  , 'is_cancelled' : 'no'
                  , 'left' : 10
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/11'
              }
            , { 'attributes' :
                  { 'boat_class' : 9
                  , 'is_cancelled' : 'no'
                  , 'left' : 10
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/MOM-Link/12'
              }
              , { 'attributes' :
                  { 'boat_class' : 7
                  , 'is_cancelled' : 'no'
                  , 'left' : 13
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/14'
              }
            , { 'attributes' :
                  { 'left' : 8
                  , 'right' : 11
                  , 'skipper' : 5
                  }
              , 'cid' : 15
              , 'pid' : 15
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/15'
              }
            , { 'attributes' :
                  { 'left' : 8
                  , 'right' : 14
                  , 'skipper' : 5
                  }
              , 'cid' : 16
              , 'pid' : 16
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/16'
                }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Link?verbose'
    }

    >>> r = show (R.get ("/v1/MOM-Link?verbose&closure"))
    { 'json' :
        { 'attribute_names' :
    [ 'left' ]
        , 'entries' :
            [ { 'attributes' :
                  { 'club' : None
                  , 'left' :
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
                  , 'mna_number' : '29676'
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 4
              , 'pid' : 4
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/4'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' :
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
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 5
              , 'pid' : 5
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/5'
              }
            , { 'attributes' :
                  { 'club' : None
                  , 'left' :
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
                  , 'mna_number' : ''
                  , 'nation' : 'AUT'
                  }
              , 'cid' : 6
              , 'pid' : 6
              , 'type_name' : 'SRM.Sailor'
              , 'url' : '/v1/MOM-Link/6'
              }
            , { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'name' : 'Optimist' }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      }
                  , 'nation' : 'AUT'
                  , 'sail_number' : '1107'
                  , 'sail_number_x' : ''
                  }
              , 'cid' : 8
              , 'pid' : 8
              , 'type_name' : 'SRM.Boat'
              , 'url' : '/v1/MOM-Link/8'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Optimist' }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
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
                  }
              , 'cid' : 11
              , 'pid' : 11
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/11'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Yardstick' }
                      , 'cid' : 9
                      , 'pid' : 9
                      , 'type_name' : 'SRM.Handicap'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
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
                  }
              , 'cid' : 12
              , 'pid' : 12
              , 'type_name' : 'SRM.Regatta_H'
              , 'url' : '/v1/MOM-Link/12'
              }
            , { 'attributes' :
                  { 'boat_class' :
                      { 'attributes' :
                          { 'name' : 'Optimist' }
                      , 'cid' : 7
                      , 'pid' : 7
                      , 'type_name' : 'SRM.Boat_Class'
                      }
                  , 'is_cancelled' : 'no'
                  , 'left' :
                      { 'attributes' :
                          { 'date' :
                              [
                                [ 'finish'
                                , '2008/06/21'
                                ]
                              ,
                                [ 'start'
                                , '2008/06/20'
                                ]
                              ]
                          , 'name' : 'Guggenberger'
                          }
                      , 'cid' : 13
                      , 'pid' : 13
                      , 'type_name' : 'SRM.Regatta_Event'
                      }
                  }
              , 'cid' : 14
              , 'pid' : 14
              , 'type_name' : 'SRM.Regatta_C'
              , 'url' : '/v1/MOM-Link/14'
              }
            , { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'name' : 'Optimist' }
                              , 'cid' : 7
                              , 'pid' : 7
                              , 'type_name' : 'SRM.Boat_Class'
                              }
                          , 'nation' : 'AUT'
                          , 'sail_number' : '1107'
                          , 'sail_number_x' : ''
                          }
                      , 'cid' : 8
                      , 'pid' : 8
                      , 'type_name' : 'SRM.Boat'
                      }
                  , 'right' :
                      { 'attributes' :
                          { 'boat_class' : 7
                          , 'left' :
                              { 'attributes' :
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
                          }
                      , 'cid' : 11
                      , 'pid' : 11
                      , 'type_name' : 'SRM.Regatta_C'
                      }
                  , 'skipper' :
                      { 'attributes' :
                          { 'club' : None
                          , 'left' :
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
                          , 'mna_number' : ''
                          , 'nation' : 'AUT'
                          }
                      , 'cid' : 5
                      , 'pid' : 5
                      , 'type_name' : 'SRM.Sailor'
                      }
                  }
              , 'cid' : 15
              , 'pid' : 15
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/15'
              }
            , { 'attributes' :
                  { 'left' :
                      { 'attributes' :
                          { 'left' :
                              { 'attributes' :
                                  { 'name' : 'Optimist' }
                              , 'cid' : 7
                              , 'pid' : 7
                              , 'type_name' : 'SRM.Boat_Class'
                              }
                          , 'nation' : 'AUT'
                          , 'sail_number' : '1107'
                          , 'sail_number_x' : ''
                          }
                      , 'cid' : 8
                      , 'pid' : 8
                      , 'type_name' : 'SRM.Boat'
                      }
                  , 'right' :
                      { 'attributes' :
                          { 'boat_class' : 7
                          , 'left' :
                              { 'attributes' :
                                  { 'date' :
                                      [
                                        [ 'finish'
                                        , '2008/06/21'
                                        ]
                                      ,
                                        [ 'start'
                                        , '2008/06/20'
                                        ]
                                      ]
                                  , 'name' : 'Guggenberger'
                                  }
                              , 'cid' : 13
                              , 'pid' : 13
                              , 'type_name' : 'SRM.Regatta_Event'
                              }
                          }
                      , 'cid' : 14
                      , 'pid' : 14
                      , 'type_name' : 'SRM.Regatta_C'
                      }
                  , 'skipper' :
                      { 'attributes' :
                          { 'club' : None
                          , 'left' :
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
                          , 'mna_number' : ''
                          , 'nation' : 'AUT'
                          }
                      , 'cid' : 5
                      , 'pid' : 5
                      , 'type_name' : 'SRM.Sailor'
                      }
                  }
              , 'cid' : 16
              , 'pid' : 16
              , 'type_name' : 'SRM.Boat_in_Regatta'
              , 'url' : '/v1/MOM-Link/16'
              }
            ]
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/MOM-Link?verbose&closure'
    }

    >>> _ = show (R.get ("/v1/pid/"))
    { 'json' :
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
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (R.get ("/v1/pid/1"))
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Christian'
            , 'last_name' : 'Tanzer'
            , 'middle_name' : ''
            , 'title' : ''
            }
        , 'cid' : 1
        , 'pid' : 1
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/MOM-Id_Entity/1'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/1'
    }

    >>> _ = show (R.get ("/v1/pid?count&strict"))
    { 'json' :
        { 'count' : 0 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count&strict'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.get ("/RAISE"))
    { 'json' :
        { 'content' : 'Wilful raisement'
        , 'description' : 'Internal server error'
        }
    , 'status' : 500
    , 'url' : 'http://localhost:9999/RAISE'
    }

    >>> server.terminate ()

"""

_test_options = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = traverse ("http://localhost:9999/")
    / : GET, HEAD, OPTIONS
    /v1/MOM-Id_Entity/1 : DELETE, GET, HEAD, OPTIONS, PUT
    /v1/PAP-Address : GET, HEAD, OPTIONS, POST

    >>> server.terminate ()

"""

_test_post = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 16 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> snoopy_cargo = json.dumps (
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
    >>> _ = show (R.post ("/v1/PAP-Person", headers=headers))
    { 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request (content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers = {}))
    { 'json' :
        { 'error' : 'You need to send the attributes defining the object with the request (content-type "application/json")' }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> r = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers=headers))
    { 'json' :
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
        , 'cid' : 17
        , 'pid' : 17
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/17'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> cargo_bir = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( left    = dict
    ...             ( left        = ["Optimist"]
    ...             , nation      = "AUT"
    ...             , sail_number = "1134"
    ...             )
    ...         , right   = 11
    ...         , skipper = dict
    ...             ( club        = dict (name = "SC-AMS")
    ...             , left        = 2
    ...             , nation      = "AUT"
    ...             )
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/SRM-Boat_in_Regatta?verbose&closure", data=cargo_bir))
    { 'json' :
        { 'attributes' :
            { 'left' :
                { 'attributes' :
                    { 'left' :
                        { 'attributes' :
                            { 'name' : 'Optimist' }
                        , 'cid' : 7
                        , 'pid' : 7
                        , 'type_name' : 'SRM.Boat_Class'
                        }
                    , 'nation' : 'AUT'
                    , 'sail_number' : '1134'
                    , 'sail_number_x' : ''
                    }
                , 'cid' : 18
                , 'pid' : 18
                , 'type_name' : 'SRM.Boat'
                }
            , 'right' :
                { 'attributes' :
                    { 'boat_class' : 7
                    , 'left' :
                        { 'attributes' :
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
                    }
                , 'cid' : 11
                , 'pid' : 11
                , 'type_name' : 'SRM.Regatta_C'
                }
            , 'skipper' :
                { 'attributes' :
                    { 'club' :
                        { 'attributes' :
                            { 'name' : 'SC-AMS' }
                        , 'cid' : 19
                        , 'pid' : 19
                        , 'type_name' : 'SRM.Club'
                        }
                    , 'left' :
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
                    , 'mna_number' : ''
                    , 'nation' : 'AUT'
                    }
                , 'cid' : 20
                , 'pid' : 20
                , 'type_name' : 'SRM.Sailor'
                }
            }
        , 'cid' : 21
        , 'pid' : 21
        , 'type_name' : 'SRM.Boat_in_Regatta'
        , 'url' : '/v1/SRM-Boat_in_Regatta/21'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta?verbose&closure'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> _ = show (R.post ("/v1/PAP-Person", data=snoopy_cargo, headers=headers))
    { 'json' :
        { 'error' : "new definition of Person (u'dog', u'snoopy', u'the', u'') clashes with existing Person (u'dog', u'snoopy', u'the', u'')" }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> cargo_c = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( last_name   = "Tin"
    ...         , first_name  = "Rin"
    ...         , middle_name = "Tin"
    ...         )
    ...     , cid = r.json ["cid"]
    ...     )
    ... )
    >>> ru = requests.utils.urlparse (r.url)
    >>> p  = "%%s://%%s%%s" %% (ru.scheme, ru.netloc, r.json ["url"])
    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'attributes' :
            { 'first_name' : 'Rin'
            , 'last_name' : 'Tin'
            , 'lifetime' :
                [
                  [ 'start'
                  , '2000/11/22'
                  ]
                ]
            , 'middle_name' : 'Tin'
            , 'title' : ''
            }
        , 'cid' : 22
        , 'pid' : 17
        , 'type_name' : 'PAP.Person'
        , 'url' : '/v1/PAP-Person/17'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person/17'
    }

    >>> s  = show (requests.put (p, data=cargo_c, headers=headers))
    { 'json' :
        { 'error' : 'Cid mismatch: requested cid = 17, current cid = 22' }
    , 'status' : 409
    , 'url' : 'http://localhost:9999/v1/PAP-Person/17'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> cargo_g = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( last_name   = "Garfield"
    ...         , first_name  = "James"
    ...         , hates       = "mondays"
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/PAP-Person", data=cargo_g, headers=headers))
    { 'json' :
        { 'error' : "Request contains invalid attribute names ('hates',)" }
    , 'status' : 400
    , 'url' : 'http://localhost:9999/v1/PAP-Person'
    }

    >>> _ = show (R.get ("/v1/pid?count"))
    { 'json' :
        { 'count' : 21 }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?count'
    }

    >>> server.terminate ()

"""

_test_query = r"""
    >>> server = run_server (%(p1)s, %(n1)s)

    >>> _ = show (R.get ("/v1/pid/"))
    { 'json' :
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
            , 14
            , 15
            , 16
            ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid/'
    }

    >>> _ = show (R.get ("/v1/pid?order_by=pid&FIRST&limit=1"))
    { 'json' :
        { 'entries' : [ 1 ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?order_by=pid&FIRST&limit=1'
    }

    >>> _ = show (R.get ("/v1/pid?order_by=pid&LAST&limit=1"))
    { 'json' :
        { 'entries' : [ 16 ]
        , 'url_template' : '/v1/MOM-Id_Entity/{entry}'
        }
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/pid?order_by=pid&LAST&limit=1'
    }

    >>> for i in range (10) :
    ...     r = R.get ("/v1/pid?order_by=pid&limit=4&offset=" + str (i))
    ...     print (i, ":", formatted_1 (r.json))
    0 : {'entries' : [1, 2, 3, 4], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    1 : {'entries' : [2, 3, 4, 5], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    2 : {'entries' : [3, 4, 5, 6], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    3 : {'entries' : [4, 5, 6, 7], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    4 : {'entries' : [5, 6, 7, 8], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    5 : {'entries' : [6, 7, 8, 9], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    6 : {'entries' : [7, 8, 9, 10], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    7 : {'entries' : [8, 9, 10, 11], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    8 : {'entries' : [9, 10, 11, 12], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}
    9 : {'entries' : [10, 11, 12, 13], 'url_template' : '/v1/MOM-Id_Entity/{entry}'}

    >>> r = show (R.get ("/v1/PAP-Person.csv?AQ=middle_name,CONTAINS,a&verbose"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime,salutation,sex'
        , 'Tanzer,Laurens,William,,,,'
        , 'Tanzer,Clarissa,Anna,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?AQ=middle_name,CONTAINS,a&verbose'
    }

    >>> r = show (R.get ("/v1/PAP-Person.csv?AQ=middle_name,EQ,&verbose"))
    { 'content' :
        [ 'last_name,first_name,middle_name,title,lifetime,salutation,sex'
        , 'Tanzer,Christian,,,,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/PAP-Person.csv?AQ=middle_name,EQ,&verbose'
    }

    >>> cargo = json.dumps (
    ...   dict
    ...     ( attributes = dict
    ...         ( left        = "Optimist"
    ...         , nation      = "AUT"
    ...         , sail_number = "1134"
    ...         )
    ...     )
    ... )
    >>> _ = show (R.post ("/v1/SRM-Boat", data=cargo))
    { 'json' :
        { 'attributes' :
            { 'left' : 7
            , 'nation' : 'AUT'
            , 'sail_number' : '1134'
            , 'sail_number_x' : ''
            }
        , 'cid' : 17
        , 'pid' : 17
        , 'type_name' : 'SRM.Boat'
        , 'url' : '/v1/SRM-Boat/17'
        }
    , 'status' : 201
    , 'url' : 'http://localhost:9999/v1/SRM-Boat'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?verbose"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?verbose'
    }

    ### API-style attribute query
    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,8&verbose"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,8&verbose'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,11&verbose"))
    { 'content' :
    [ 'left,right,skipper,place,points' ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=left,EQ,11&verbose'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=right,EQ,11&verbose"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=right,EQ,11&verbose'
    }

    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?AQ=skipper,EQ,5&verbose"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?AQ=skipper,EQ,5&verbose'
    }

    ### HTML-form-style attribute query
    >>> r = show (R.get ("/v1/SRM-Boat_in_Regatta.csv?left___EQ=8&verbose"))
    { 'content' :
        [ 'left,right,skipper,place,points'
        , '8,11,5,,'
        , '8,14,5,,'
        ]
    , 'status' : 200
    , 'url' : 'http://localhost:9999/v1/SRM-Boat_in_Regatta.csv?left___EQ=8&verbose'
    }

    >>> server.terminate ()

"""

_test_qr_local = """

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> b4  = SRM.Boat ("Optimist", "AUT", "1134", raw = True)
    >>> print (b4.pid, b4)
    17 ((u'optimist', ), u'AUT', 1134, u'')

    >>> SRM.Boat_in_Regatta.AQ.boat
    <left.AQ [Attr.Type.Querier Id_Entity]>
    >>> SRM.Boat_in_Regatta.AQ.boat.EQ
    <Attr.Id_Entity_Equal left.EQ [==]>
    >>> SRM.Boat_in_Regatta.AQ.boat.EQ ("8")
    Q.left == 8

    >>> SRM.Boat_in_Regatta.query_s ().all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]

    >>> b7 = SRM.Boat.query (sail_number = 1107).one ()
    >>> print (b7.pid, b7)
    8 ((u'optimist', ), u'AUT', 1107, u'')

    >>> SRM.Boat_in_Regatta.query_s (boat = b7).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (boat = 8).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (boat = "8").all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]

    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ (8)).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]
    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ ("8")).all ()
    [SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'guggenberger', dict (start = u'2008/06/20', finish = u'2008/06/21')), (u'optimist', ))), SRM.Boat_in_Regatta (((u'optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'optimist', )))]

    >>> SRM.Boat_in_Regatta.query_s (boat = b4).all ()
    []
    >>> SRM.Boat_in_Regatta.query_s (boat = 17).all ()
    []
    >>> SRM.Boat_in_Regatta.query_s (SRM.Boat_in_Regatta.AQ.boat.EQ ("17")).all ()
    []

    >>> scope.destroy ()

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_cqf        = _test_cqf
        , test_delete     = _test_delete
        , test_doc        = _test_doc
        , test_example_1  = _test_example_1
        , test_example_2  = _test_example_2
        , test_example_3  = _test_example_3
        , test_example_4  = _test_example_4
        , test_get        = _test_get
        , test_options    = _test_options
        , test_post       = _test_post
        , test_query      = _test_query
        , test_qr_local   = _test_qr_local
        )
    )

if __name__ == "__main__" :
    backend = sos.environ.get \
        ("GTW_test_backends", ("HPS")).split (":") [0].strip ()
    db_url = Scaffold.Backend_Parameters.get (backend, "hps://").strip ("'")
    _run_server (["-db_url", db_url, "-db_name", "test", "-debug", "no"])
### __END__ GTW.__test__.RST
