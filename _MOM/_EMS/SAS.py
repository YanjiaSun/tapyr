# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.EMS.SAS
#
# Purpose
#    Entity manager strategy using SQL layer from SQLAlchemy
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based of MOM.EMS.SA)
#    27-Mar-2010 (MG) `add` support for `polymorphic_epk` added
#    12-May-2010 (MG) Use new `pid_manager`, lid functions changed
#    12-May-2010 (CT) `pid_as_lid` and `pid_from_lid` removed
#    17-May-2010 (CT) Class `PID` removed
#    17-May-2010 (MG) `add` parameter `id` added
#     1-Jul-2010 (MG) `pcm` and `max_pid` added
#     5-Jul-2010 (MG) `load_root` and `register_scope` are now method's of
#                     the session
#    15-Aug-2010 (MG) `pid_query` added
#    ��revision-date�����
#--

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.I18N             import _, _T, _Tn

import _MOM._EMS._Manager_
import _MOM.Entity
import _MOM._DBW._SAS.Q_Result
import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy  import exc        as SAS_Exception
from   sqlalchemy  import sql

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name = "SAS"

    Q_Result  = MOM.DBW.SAS.Q_Result

    def add (self, entity, id = None) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        if entity.polymorphic_epk :
            ### since we have a polymorphic epk the database layer cannot
            ### check the name clash -> therefore we need to make an extra
            ### query for this.
            existing = self.instance (entity.__class__, entity.epk)
            if existing :
                raise MOM.Error.Name_Clash (entity, existing)
        max_c = entity.max_count
        if max_c and max_c <= self.query (entity.__class__).count () :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity, id)
        except SAS_Exception.IntegrityError as exc :
            ses.rollback ()
            if __debug__ :
                print exc
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
    # end def add

    def changes (self, * filter, ** eq_kw) :
        query = MOM.DBW.SAS.Q_Result_Changes \
            (MOM.SCM.Change._Change_, self.session).filter (* filter, ** eq_kw)
        return query
    # end def changes

    def load_root (self) :
        result            = self.session.load_root (self.scope)
        self.scope.db_cid = self.max_cid
        return result
    # end def load_root

    def pid_query (self, pid, Type) :
        pid        = int (pid)
        result     = self.session.pid_query (pid)
        if result is None :
            result = self.pm.query          (pid)
        if not isinstance (result, Type.Essence) :
            raise LookupError \
                ( "Pid `%r` is instance of type %s, not of type `%s`"
                % (pid, result.type_name, Type.type_name)
                )
        return result
    # end def pid_query

    @property
    def max_cid (self) :
        id_col   = MOM.SCM.Change._Change_._sa_table.c.cid
        last     = self.session.execute \
            ( sql.select ((id_col, )).order_by (id_col.desc ()).limit (1)
            ).fetchone ()
        return (last and last.cid) or 0
    # end def max_cid

    @property
    def max_pid (self) :
        return self.scope.ems.pm.max_pid
    # end def max_cid

    @property
    def pcm (self) :
        return self.session
    # end def pcm

    def register_change (self, change) :
        self.session.add_change (change)
        ###self.session.flush  ()
        if change.children :
            Table  = MOM.SCM.Change._Change_._sa_table
            update = Table.update ().where \
                ( Table.c.cid.in_ (c.cid for c in change.children)
                ).values (parent_cid = change.cid)
            self.session.execute (update)
        self.scope.db_cid = change.cid
        self.__super.register_change (change)
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        self.session.register_scope (self.scope)
    # end def register_scope

    def remove (self, entity) :
        self.session.delete (entity)
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.__class__, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        renamer     ()
    # end def rename

    def _query_multi_root (self, Type) :
        QR = self.Q_Result
        S  = self.session
        return self.Q_Result_Composite \
            ([QR (t, self.session) for t in Type.relevant_roots.itervalues ()])
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        Type = getattr (Type, "_etype", Type)
        return self.Q_Result (Type, self.session)
    # end def _query_single_root

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SAS
