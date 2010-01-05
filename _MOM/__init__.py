# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This file is part of the package _MOM.
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
# along with this package.  If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.__init__
#
# Purpose
#    Package implementing a simple meta object model in python
#
# Revision Dates
#    17-Sep-2009 (CT) Creation (factored from TOM)
#    ��revision-date�����
#--

from _TFL.Package_Namespace import Package_Namespace

MOM = Package_Namespace ()

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM` provides a framework for the definition and
implementation of essential object models.

An essential (see [McP84]_) object model is one, IMHO the best, way of
capturing the results of an object oriented analysis. An essential
object model comprises classes and associations.

Each essential class (modelled by a descendent of the class
:class:`MOM.Object<_MOM.Object.Object>`)
describes one specific type of object, in particluar

- the attributes (modelled by the classes in the package namespace
  :mod:`MOM.Attr<_MOM._Attr>`),

- and the predicates (modelled by the classes in the package namespace
  :mod:`MOM.Pred<_MOM._Pred>`)

visible to the class' clients.

Each essential association (modelled by a descendent of the class
:class:`MOM.Link<_MOM.Link.Link>`)
describes the possible links between the objects of a number of classes.

As the links of an association are also characterized by attributes
and predicates, most of the behavior of
:class:`MOM.Object<_MOM.Object.Object>` and
:class:`MOM.Link<_MOM.Link.Link>` is defined by their common ancestor
:class:`MOM.Id_Entity<_MOM.Entity.Id_Entity>`.

A specific meta object model is defined for a well-defined application. Each
instance of a meta object model is managed by a scope object (modelled by the
class :class:`MOM.Scope<_MOM.Scope.Scope>`).

"""

### __END__ MOM.__init__
