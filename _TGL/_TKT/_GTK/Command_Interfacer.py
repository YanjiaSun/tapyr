# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Command_Interfacer
#
# Purpose
#    Model command interface for GTK based GUI
#
# Revision Dates
#     8-Apr-2005 (MG) Creation
#    ��revision-date�����
#--
from   _TFL.predicate       import dict_from_list
from   _TGL                 import TGL
from   _TFL.Regexp          import *
from    NO_List             import NO_List
import _TGL._TKT._GTK
import _TGL._TKT.Command_Interfacer
import _TGL._TKT._GTK.Menu
import _TGL._TKT._GTK.Menu_Bar
import _TGL._TKT._GTK.Menu_Item
import _TGL._TKT._GTK.Separator_Menu_Item

import _TGL._TKT._GTK.Toolbar
import _TGL._TKT._GTK.Tool_Button
import _TGL._TKT._GTK.Separator_Tool_Item
import _TGL._TKT._GTK.Image

import  weakref
import  traceback

GTK = TGL.TKT.GTK

### todo
### - icon support for images
### - toggle support
### - groups inside a toolbar group
### - Implement CI_Button_Box

class Boolean_Variable (object) :
    """Variable used by the Command Manager for a checkbox style command
       interfacer element.
    """

    def __init__ (self, default = True, states = (False, True)) :
        self._state            = default
        self._clients          = weakref.WeakKeyDictionary
    # end def __init__

    def register (self, client) :
        self._clients [client] = True
    # end def register

    def unregister (self, client) :
        del self._clients [client]
    # end def unregister

    def _set_state (self, state) :
        if self._state != state :
            self._state = state
            for c in self._clients.iterkeys () :
                c.state = state
    # end def _set_state

    state = property (lambda s : s._state, _set_state)

# end class Boolean_Variable

class _CI_ (TFL.TKT.Command_Interfacer) :
    """Base class for all command interfacers"""

    def _push_help (self, event = None) :
        print "Push Help for", self
    # end def _push_help

    def _pop_help (self, event = None) :
        print "Pop Help for", self
    # end def _pop_help

# end class _CI_

class CI_Button_Box (_CI_) :
    """Implement a button box command interfacer for GTK"""

    def __init__ (self, * args, ** kw) :
        raise NotImplementedError
    # end def __init__

# end class CI_Button_Box

class CI_Event_Binder (_CI_) :
    """Implement an event-bound interfacer for Tkinter (i.e., commands
       triggered by key-presses, mouse-clicks and other such events)
    """

    def __init__ (self, AC = None, * widgets) :
        self.__super.__init__ (AC = AC)
        self.bindings = {}
        self.widgets  = dict_from_list (widgets)
    # end def __init__

    def add_widget (self, * widgets) :
        for w in widgets :
            self.widgets [w] = None
        ### a new widget has been added -> enable the bindings
        for name in sekf.bindings.iterkeys () :
            self.enable_entry (name)
    # end def add_widget

    def remove_widget (self, * widgets) :
        for w in widgets :
            try :
                del self.widgets [w]
            except KeyError :
                pass
    # end def remove_widget

    def destroy (self) :
        for b in self.bindings.iterkeys () :
            self.disable_entry (b)
        self.widgets  = None
        self.bindings = None
    # end def destroy

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        info                 = info or name
        event                = getattr (self.TNS.Eventname, info)
        self.bindings [name] = [event, callback, []]
        ### all other command interfacers (menu, toolbar) are enabled by
        ### default -> enable the binding as well
        self.enable_entry (name)
    # end def add_command

    def remove_command (self, index) :
        self.disable_entry (index)
        del self.bindings  [index]
    # end def remove_command

    ### event specific methods
    def enable_entry (self, index) :
        signal, callback, conn_ids = self.bindings [index]
        self.disable_entry (index)
        conn_ids = self.bindings [index] [-1]
        for w in self.widgets :
            conn_ids.append ((w, signal.bind_add (w, callback)))
    # end def enable

    def disable_entry (self, index) :
        signal, callback, conn_ids = self.bindings [index]
        for w, cid in conn_ids :
            signal.unbind (w, cid)
        self.bindings [index] [-1] = []
    # end def disable_entry

# end class CI_Event_Binder

class _CI_Item_Mixin_ (_CI_) :
    """Base class for all command interfacers using a `NO_List` to store the
       position of the `child`
    """

    def __init__ (self, balloon = None, help = None, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._items      = NO_List ()
        self.balloon     = balloon
        self.help_widget = help
    # end def __init__

    def index (self, name) :
        return self._items [name]
    # end def index

    ### command specific methods
    def add_command ( self, name, callback
                    , index           = None
                    , delta           = 0
                    , underline       = None
                    , accelerator     = None
                    , icon            = None
                    , info            = None
                    , state_var       = None
                    , cmd_name        = None
                    , ** kw
                    ) :
        if state_var is not None :
            fct = self._new_check_item
            kw ["variable"] = state_var
        else :
            fct = self._new_item
        return self._insert_item \
            ( index, delta
            , fct
                ( label       = name
                , command     = callback
                , underline   = underline
                , icon        = icon
                , accelerator = accelerator
                , ** kw
                )
            )
    # end def add_command

    def remove_command (self, index) :
        self._remove (index)
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        item, result = self._new_group (name)
        self._insert_item              (index, delta, item)
        return result
    # end def add_group

    def remove_group (self, index) :
        self._remove (index)
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        item =  self.Separator_Class ()
        return self._insert_item     (index, delta, item)
    # end def add_separator

    def remove_separator (self, index) :
        self._remove (index)
    # end def remove_separator

    def enable_entry (self, name) :
        try :
            self._items [name].sensitive = True
        except (KeyError, AttributeError) :
            if 1 and __debug__ :
                traceback.print_exc ()
                print "Enable_entry", self, name
    # end def enable

    def disable_entry (self, name) :
        try :
            self._items [name].sensitive = False
        except (KeyError, AttributeError) :
            if 1 and __debug__ :
                traceback.print_exc ()
                print "Disable_entry", self, name
    # end def disable_entry

# end class _CI_Item_Mixin_

class _CI_Menu_Mixin_ (_CI_Item_Mixin_) :
    """Mixin for menu and menubar"""

    Separator_Class = GTK.Separator_Menu_Item

    def _new_group (self, name) :
        item             = self.TNS.Menu_Item \
            ( label      = name
            # XXX underline
            )
        item.submenu = menu = CI_Menu \
            ( AC         = self.AC
            , name       = name
            , balloon    = self.balloon
            , help       = self.help_widget
            )
        menu.show         ()
        return item, menu
    # end def _new_group

    def _new_item ( self
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        ### handle underline, icon, and accelerator
        item = GTK.Menu_Item (label = label, name = label)
        if command :
            item.bind_add (self.TNS.Signal.Activate, command)
        if self.help_widget :
            item.bind_add (self.TNS.Signal.Select,   self._push_help)
            item.bind_add (self.TNS.Signal.Deselect, self._pop_help)
        return item
    # end def _new_item

    def _insert_item (self, index, delta, item) :
        ### insert the new item to the `_items` NO-list and add the new item
        ### to the menu/menubar/toolbar
        self._items.insert (index, item, delta)
        self.insert        (item, self._items.n_index  (item.name))
        item.show          ()
        return item
    # end def _insert_item

    def _remove (self, index) :
        item = self._items [index]
        del self._items    [index]
        self.remove (item)
    # end def _remove

# end class _CI_Menu_Mixin_

class CI_Menu (_CI_Menu_Mixin_, GTK.Menu) :
    """Implement a menu command interfacer for GTK"""

    ### event specific methods
    def bind_to_activation (self, callback) :
        self.wtk_object.bind_add (self.TNS.Realize, callback)
    # end def bind_to_activation

    def bind_to_widget (self, widget, event_name) :
        ### use Event_Name/Event_Binder for the event_name <-> event_name
        event = getattr (self.TNS.Eventname, event_name)
        widget.bind_add (event, self.popup)
    # end def bind_to_widget

# end class CI_Menu

class CI_Menubar (_CI_Menu_Mixin_, GTK.Menu_Bar) :
    """Implement a menubar command interfacer for GTK"""

    def bind_to_sync (self, callback) :
        self.bind_replace (self.TNS.Signal.Enter_Notify, callback)
    # end def bind_to_sync

# end class CI_Menubar

class _CI_Toolbar_Mixin_ (_CI_Item_Mixin_) :

    Separator_Class  = GTK.Separator_Tool_Item
    group_seperators = 0

    def _insert_item (self, index, delta, item, correction = 0) :
        self._items.insert        (index, item, delta)
        pos = self._items.n_index (item.name)
        if isinstance (item, GTK.Tool_Item) :
            self.insert    (item, pos + correction)
            item.show      ()
        else :
            if len (self._items) > 1 :
                ### a group inserted as first group
                pos = 1
            if pos > 0 :
                ### this is a group which is not the first, so let's insert and
                ### seperator
                g = _CI_Toolbar_Group_ \
                    ( name    = "GS_%d" % self.group_seperators
                    , toolbar = item.toolbar
                    , balloon = item.balloon
                    , help    = item.help_widget
                    , AC      = self.AC
                    )
                self.__class__.group_seperators += 1
                self._items.insert     (pos, g)
                g.add_separator        ()
        return item
    # end def _insert_item

    def _remove (self, index) :
        item = self._items [index]
        del self._items    [index]
        self.remove (item)
    # end def _remove

    def _new_item ( self
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        if icon :
            icon = GTK.Image \
                (stock_id = icon, size = GTK.gtk.ICON_SIZE_SMALL_TOOLBAR)
            icon.show ()
        item = GTK.Tool_Button (icon= icon, label = label, name = label)
        if command :
            item.bind_add (self.TNS.Signal.Clicked, command)
        if self.help_widget :
            item.bind_add (self.TNS.Signal.Enter_Notify, self._push_help)
            item.bind_add (self.TNS.Signal.Leave_Notify, self._pop_help)
        return item
    # end def _new_item

# end class _CI_Toolbar_Mixin_

class CI_Toolbar (_CI_Toolbar_Mixin_, GTK.Toolbar) :
    """Implement a toolbar command interfacer for GTK"""

    Separator_Class = GTK.Separator_Menu_Item

    def bind_to_sync (self, callback) :
        self.bind_replace (self.TNS.Signal.Enter_Notify, callback)
    # end def bind_to_sync

    def _new_group (self, name) :
        group = _CI_Toolbar_Group_ \
            ( name    = name
            , toolbar = self
            , balloon = self.balloon
            , help    = self.help_widget
            , AC      = self.AC
            )
        return group, group
    # end def _new_group

# end class CI_Toolbar

class _CI_Toolbar_Group_ (_CI_Toolbar_Mixin_) :

    insert = property (lambda s : s.toolbar.insert)
    remove = property (lambda s : s.toolbar.remove)

    def __init__ (self, AC, name, toolbar, balloon = None, help = None) :
        self.__super.__init__ (AC = AC, balloon = balloon, help = help)
        self.name         = name
        self.toolbar      = toolbar
    # end def __init__

    def _insert_item (self, index, delta, item) :
        correction = 0
        for i in range (self.toolbar._items.n_index (self.name)) :
            correction += len (self.toolbar._items [i])
        result = self.__super._insert_item (index, delta, item, correction)
        return result
    # end def _insert_item

    def __len__ (self) : return len (self._items)

# end class _CI_Toolbar_Group_

if __name__ != "__main__" :
    TGL.TKT.GTK._Export ("*")
### __END__ TGL.TKT.GTK.Command_Interfacer


