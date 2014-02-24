# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.Document_Link
#
# Purpose
#    Test how generic links to object without a relevant root work,
#
# Revision Dates
#    27-Oct-2010 (MG) Creation
#    29-Mar-2012 (CT) Add test for `link_map`
#     4-Jun-2012 (MG) Test for query with order_by added
#     6-Jun-2012 (CT) Add test for `Entity_created_by_Person.sort_key`
#    12-Jun-2012 (CT) Add `date` to get deterministic output
#     3-Aug-2012 (CT) Add tests for `Ref_Req_Map` and `Ref_Opt_Map`
#     3-Aug-2012 (CT) Use `Ref_Req_Map`, not `link_map`
#    12-Sep-2012 (RS) Add `Id_Entity`
#     6-Dec-2012 (CT) Add `PAP.Person_has_Account`
#    20-Jan-2013 (CT) Add `Auth.Certificate`
#     4-Mar-2013 (CT) Add `PAP.Legal_Entity`
#    28-Jul-2013 (CT) Replace `tn_pid` by `type_name` and `pid`
#    ««revision-date»»···
#--

test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> date = (("start", "2012/06/10"), )
    >>> MOM  = scope.MOM
    >>> PAP  = scope.PAP
    >>> SWP  = scope.SWP
    >>> per  = PAP.Person ("ln", "fn")
    >>> pa1  = SWP.Page   ("title_1", text = "text 1", date = date, raw = True)
    >>> pa2  = SWP.Page   ("title_2", text = "text 2", date = date, raw = True)
    >>> pa3  = SWP.Page   ("title_3", text = "text 3", date = date, raw = True)
    >>> scope.commit     ()

    >>> _ = MOM.Document (per, "//foo.bar/baz")
    >>> _ = MOM.Document (per, "//foo.bar/qux")
    >>> _ = MOM.Document (pa1, "//foo.bar/quux.jpg")
    >>> scope.commit ()

    >>> q  = MOM.Document.query ()
    >>> qs = MOM.Document.query_s ()
    >>> q.order_by (Q.pid).all ()
    [MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/baz', u''), MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/qux', u''), MOM.Document ((u'title_1', ), u'//foo.bar/quux.jpg', u'')]

    >>> q.order_by (TFL.Sorted_By ("pid")).all ()
    [MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/baz', u''), MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/qux', u''), MOM.Document ((u'title_1', ), u'//foo.bar/quux.jpg', u'')]

    >>> q.order_by (MOM.Document.sorted_by).all ()
    [MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/baz', u''), MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/qux', u''), MOM.Document ((u'title_1', ), u'//foo.bar/quux.jpg', u'')]

    >>> qs.all ()
    [MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/baz', u''), MOM.Document ((u'ln', u'fn', u'', u''), u'//foo.bar/qux', u''), MOM.Document ((u'title_1', ), u'//foo.bar/quux.jpg', u'')]

    >>> q = scope.query_changes (type_name = "SWP.Page").order_by (Q.cid)
    >>> for c in q.all () :
    ...     print c
    <Create SWP.Page (u'title_1', 'SWP.Page'), new-values = {'contents' : u'<p>text 1</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '2', 'text' : u'text 1'}>
    <Create SWP.Page (u'title_2', 'SWP.Page'), new-values = {'contents' : u'<p>text 2</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '3', 'text' : u'text 2'}>
    <Create SWP.Page (u'title_3', 'SWP.Page'), new-values = {'contents' : u'<p>text 3</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '4', 'text' : u'text 3'}>

    >>> scope.MOM.Id_Entity.query ().order_by (Q.pid).attrs ("type_name", "pid").all ()
    [('PAP.Person', 1), ('SWP.Page', 2), ('SWP.Page', 3), ('SWP.Page', 4), ('MOM.Document', 5), ('MOM.Document', 6), ('MOM.Document', 7)]

    >>> show_ref_maps (scope, "Ref_Req_Map")
    MOM.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM._MOM_Link_n_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Link2
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Link3
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    MOM.Document
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth._Account_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_Anonymous
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account
        ('Auth.Account_Activation', ['left'])
        ('Auth.Account_EMail_Verification', ['left'])
        ('Auth.Account_Password_Change_Required', ['left'])
        ('Auth.Account_Password_Reset', ['left'])
        ('Auth.Account_in_Group', ['left'])
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Person_has_Account', ['right'])
    Auth.Certificate
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Group
        ('Auth.Account_in_Group', ['right'])
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth._MOM_Link_n_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Link2
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_in_Group
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth._Account_Action_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_Activation
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_Password_Change_Required
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth._Account_Token_Action_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_EMail_Verification
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    Auth.Account_Password_Reset
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Calendar
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Event
        ('EVT.Event', ['left'])
        ('EVT.Event_occurs', ['left'])
        ('EVT.Recurrence_Spec', ['left'])
        ('MOM.Document', ['left'])
    EVT.Event_occurs
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT._Recurrence_Mixin_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    EVT.Recurrence_Spec
        ('EVT.Event', ['left'])
        ('EVT.Recurrence_Rule', ['left'])
        ('MOM.Document', ['left'])
    EVT.Recurrence_Rule
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Property
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Address
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Address_Position', ['left'])
        ('PAP.Company_has_Address', ['right'])
        ('PAP.Person_has_Address', ['right'])
    PAP.Subject
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Legal_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Company
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Company_has_Address', ['left'])
        ('PAP.Company_has_Email', ['left'])
        ('PAP.Company_has_Phone', ['left'])
        ('PAP.Company_has_Url', ['left'])
    PAP.Email
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Company_has_Email', ['right'])
        ('PAP.Person_has_Email', ['right'])
    PAP.Phone
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Company_has_Phone', ['right'])
        ('PAP.Person_has_Phone', ['right'])
    PAP.Person
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Person_has_Account', ['left'])
        ('PAP.Person_has_Address', ['left'])
        ('PAP.Person_has_Email', ['left'])
        ('PAP.Person_has_Phone', ['left'])
        ('PAP.Person_has_Url', ['left'])
        ('SRM.Sailor', ['left'])
    PAP.Url
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('PAP.Company_has_Url', ['right'])
        ('PAP.Person_has_Url', ['right'])
    PAP.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Address_Position
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP._MOM_Link_n_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Link2
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Subject_has_Property
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Person_has_Account
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM._Boat_Class_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Boat_Class
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat', ['left'])
        ('SRM.Regatta_C', ['boat_class'])
    SRM.Handicap
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Regatta_H', ['boat_class'])
    SRM.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Boat
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat_in_Regatta', ['left'])
    SRM.Club
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Regatta_Event
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Page', ['event'])
        ('SRM.Regatta_C', ['left'])
        ('SRM.Regatta_H', ['left'])
    SWP.Id_Entity
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Object
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Object_PN
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Page
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Page_Y
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Link
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Link1
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Clip_O
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Clip_X
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Gallery
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
        ('SWP.Picture', ['left'])
    SWP.Picture
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SWP.Referral
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SRM.Page
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SWP.Clip_O', ['left'])
    SRM.Regatta
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
    SRM.Regatta_C
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
        ('SRM.Team', ['left'])
    SRM.Regatta_H
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
    SRM.Sailor
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Boat_in_Regatta', ['skipper'])
        ('SRM.Crew_Member', ['right'])
    SRM._MOM_Link_n_
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Link2
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Boat_in_Regatta
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Crew_Member', ['left'])
        ('SRM.Race_Result', ['left'])
        ('SRM.Team_has_Boat_in_Regatta', ['right'])
    SRM.Race_Result
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Team
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
        ('SRM.Team_has_Boat_in_Regatta', ['left'])
    SRM.Crew_Member
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    SRM.Team_has_Boat_in_Regatta
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Subject_has_Address
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Subject_has_Email
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Subject_has_Phone
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Subject_has_Url
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Company_has_Url
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Person_has_Url
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Company_has_Phone
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Person_has_Phone
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Company_has_Email
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Person_has_Email
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Company_has_Address
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])
    PAP.Person_has_Address
        ('EVT.Event', ['left'])
        ('MOM.Document', ['left'])


    >>> show_ref_maps (scope, "Ref_Opt_Map")
    EVT.Calendar
        ('EVT.Event', ['calendar'])
    PAP.Person
        ('SRM.Team', ['leader'])
    SRM.Club
        ('SRM.Regatta_Event', ['club'])
        ('SRM.Sailor', ['club'])
        ('SRM.Team', ['club'])

"""

import _MOM.Document
from   _GTW.__test__.model      import *
from   _TFL.Formatter           import formatted_1

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Document_Link
