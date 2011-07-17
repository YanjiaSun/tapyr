# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.__test__.
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
#    MOM.__test__.Person
#
# Purpose
#    Test PAP.Person creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#     5-Jul-2011 (CT) `MOM.Attr.Selector` tests added
#     6-Jul-2011 (CT) Tests for `f_completer` added
#    17-Jul-2011 (CT) s/f_completer/completer/, completion tests added
#    ��revision-date�����
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> print PAP.Person.count
    0
    >>> PAP.Person.instance_or_new ("Tanzer", "Christian") ### 1
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> print PAP.Person.count
    1
    >>> PAP.Person.instance ("Tanzer", "Christian")
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> PAP.Person.query_s ().all ()
    [GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> PAP.Person.instance_or_new ("Tanzer", "Christian") ### 2
    GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')
    >>> print PAP.Person.count
    1

    >>> _ = PAP.Person ("Tanzer", "Egon")
    >>> _ = PAP.Person ("Tanzer", "Walter")
    >>> _ = PAP.Person ("Tanzer", "Martin")
    >>> _ = PAP.Person ("Tanzer", "Michael")

    >>> S = MOM.Attr.Selector
    >>> S.primary (PAP.Person).names
    ('last_name', 'first_name', 'middle_name', 'title')
    >>> S.Combo (S.primary, exclude = S.P_optional) (PAP.Person).names
    ('last_name', 'first_name')
    >>> S.Combo (S.primary, exclude = S.P_required) (PAP.Person).names
    ('middle_name', 'title')
    >>> S.necessary (PAP.Person).names
    ('sex',)
    >>> S.optional (PAP.Person).names
    ('lifetime', 'salutation')
    >>> S.required (PAP.Person).names
    ()
    >>> S.user (PAP.Person).names
    ('lifetime', 'salutation', 'sex')
    >>> pu = S.List (S.primary, S.user)
    >>> pu (PAP.Person).names
    ('last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'salutation', 'sex')
    >>> S.Combo (pu, exclude = S.P_optional) (PAP.Person).names
    ('last_name', 'first_name')
    >>> S.Combo (pu, exclude = S.P_required) (PAP.Person).names
    ('middle_name', 'title', 'lifetime', 'salutation', 'sex')

    >>> lnc = PAP.Person.last_name.completer (PAP.Person.last_name, PAP.Person)
    >>> print lnc.name, lnc.names, lnc.treshold
    last_name ('last_name', 'first_name', 'middle_name', 'title') 2
    >>> fnc = PAP.Person.first_name.completer (PAP.Person.first_name, PAP.Person)
    >>> print fnc.name, fnc.names, fnc.treshold
    first_name ('first_name', 'last_name', 'middle_name', 'title') 3
    >>> tnc = PAP.Person.title.completer (PAP.Person.title, PAP.Person)
    >>> print tnc.name, tnc.names, tnc.treshold
    title ('title',) 1
    >>> snc = PAP.Person.salutation.completer (PAP.Person.salutation, PAP.Person)
    >>> print snc.name, snc.names, snc.treshold
    salutation ('salutation',) 1

    >>> sorted (lnc (scope, dict (last_name = "Ta")))
    [(u'tanzer', u'christian', u'', u''), (u'tanzer', u'egon', u'', u''), (u'tanzer', u'martin', u'', u''), (u'tanzer', u'michael', u'', u''), (u'tanzer', u'walter', u'', u'')]
    >>> sorted (lnc (scope, dict (last_name = "Ta", first_name = "M")))
    [(u'tanzer', u'martin', u'', u''), (u'tanzer', u'michael', u'', u'')]
    >>> sorted (lnc (scope, dict (last_name = "Ta", first_name = "Ma")))
    [(u'tanzer', u'martin', u'', u'')]
    >>> sorted (lnc (scope, dict (last_name = "Ta", title = "Mag.")))
    []

    >>> sorted (lnc (scope, dict (last_name = "Ta"), complete_entity = True))
    [(u'tanzer', u'christian', u'', u'', 1, 1), (u'tanzer', u'egon', u'', u'', 2, 2), (u'tanzer', u'martin', u'', u'', 4, 4), (u'tanzer', u'michael', u'', u'', 5, 5), (u'tanzer', u'walter', u'', u'', 3, 3)]
    >>> sorted (lnc (scope, dict (last_name = "Ta", first_name = "Ma"), complete_entity = True))
    [(u'tanzer', u'martin', u'', u'', 4, 4)]

"""

from   _GTW.__test__.model      import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ MOM.__test__.Person
