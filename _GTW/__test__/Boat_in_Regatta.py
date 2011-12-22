# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
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
#    GTW.__test__.Boat_in_Regatta
#
# Purpose
#    Test creation and querying of Boat_in_Regatta
#
# Revision Dates
#     3-May-2010 (MG) Creation
#     3-May-2010 (CT) Creation continued
#    14-Dec-2011 (CT) Add tests for `attrs`
#    ��revision-date�����
#--

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
    >>> list (r.name for r in sorted (rev.regattas))
    [u'Optimist', u'Yardstick']

    >>> reg.set_raw (result = dict (date = "26.5.2009 10:20", software = u"calculated with REGATTA.yellow8.com", status = "final", raw = True))
    1
    >>> unicode (reg.FO.result)
    u'2009/05/26 10:20:00, calculated with REGATTA.yellow8.com, final'
    >>> scope.commit ()

    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event')
    >>> reg.epk_raw
    ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C')
    >>> SRM.Regatta_C.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))
    >>> SRM.Regatta.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))
    >>> SRM.Regatta_C.instance (* reg.epk_raw, raw = True)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))

    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
    >>> bir.epk_raw
    (((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta')
    >>> SRM.Boat_in_Regatta.instance (* bir.epk_raw, raw = True)
    GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))

    >>> BiR = SRM.Boat_in_Regatta
    >>> sort_key = TFL.Sorted_By ("-regatta.event.date.start", "skipper.person.last_name", "skipper.person.first_name")

    >>> print sort_key
    <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>
    >>> print BiR.E_Type.sort_key_pm (sort_key)
    <Sorted_By: Getter function for `.relevant_root.type_name`, <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>>

    >>> list (BiR.query (sort_key = sort_key))
    [GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))]
    >>> list (BiR.query_s (sort_key = sort_key))
    [GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', 1107, u''), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))]

    >>> df = SRM.Regatta.AQ.event.date.start.EQ ("2008")
    >>> df
    Q.left.date.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31))

    >>> AQ  = BiR.AQ.Select (MOM.Attr.Selector.sig)
    >>> q   = SRM.Regatta.query_s ().filter (df)
    >>> fs  = tuple (x.QR for x in AQ.regatta.Unwrapped_Atoms)
    >>> fsn = tuple (x._name for x in fs)
    >>> fss = ('left.__raw_name', 'left.date')
    >>> fst = ('left', )

    >>> AQ
    <Attr.Type.Querier.E_Type for GTW.OMP.SRM.Boat_in_Regatta>
    >>> AQ._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>
    >>> AQ.left._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>
    >>> AQ.right.left.date._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>

    >>> fs
    (Q.left.__raw_name, Q.left.date.start, Q.left.date.finish)

    >>> list (q)
    [GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )), GTW.OMP.SRM.Regatta_H ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), u'Yardstick')]

    >>> list (q.attrs (* fs))
    [(u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1)), (u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1))]

    >>> list (q.attrs (* fsn))
    [(u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1)), (u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1))]

    >>> list (q.attrs (* fss))
    [(u'Himmelfahrt', MOM.Date_Interval_C (finish = 2008/05/01, start = 2008/05/01)), (u'Himmelfahrt', MOM.Date_Interval_C (finish = 2008/05/01, start = 2008/05/01))]

    >>> list (q.attrs (* fst))
    [(GTW.OMP.SRM.Regatta_Event (u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')),), (GTW.OMP.SRM.Regatta_Event (u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')),)]

    >>> AQ  = BiR.AQ.Select (MOM.Attr.Selector.all)
    >>> AQ
    <Attr.Type.Querier.E_Type for GTW.OMP.SRM.Boat_in_Regatta>
    >>> AQ._attr_selector
    <MOM.Attr.Selector.List ['<MOM.Attr.Selector.Kind primary>', '<MOM.Attr.Selector.Kind user_attr>', '<MOM.Attr.Selector.Kind query>']>
    >>> AQ.left._attr_selector
    <MOM.Attr.Selector.List ['<MOM.Attr.Selector.Kind primary>', '<MOM.Attr.Selector.Kind user_attr>', '<MOM.Attr.Selector.Kind query>']>
    >>> AQ.right.left.date._attr_selector
    <MOM.Attr.Selector.List ['<MOM.Attr.Selector.Kind primary>', '<MOM.Attr.Selector.Kind user_attr>', '<MOM.Attr.Selector.Kind query>']>

    >>> tuple (x.QR for x in AQ.regatta.Atoms)
    (Q.right.left.__raw_name, Q.right.left.date.start, Q.right.left.date.finish, Q.right.left.date.alive, Q.right.left.club.__raw_name, Q.right.left.club.long_name, Q.right.left.desc, Q.right.discards, Q.right.kind, Q.right.races, Q.right.result.date, Q.right.result.software, Q.right.result.status)

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat_in_Regatta
