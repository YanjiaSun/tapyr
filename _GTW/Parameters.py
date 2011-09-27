# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Parameters
#
# Purpose
#    Support definition of parameters for media, i.e., CSS and JS, fragments
#
# Revision Dates
#    14-Jan-2011 (CT) Creation
#    13-Sep-2011 (CT) `Script_File` and `Style_File` added
#    13-Sep-2011 (MG) doctest added
#    27-Sep-2011 (MG) `Include`, `Eval`, and `_eval_file` added
#    ��revision-date�����
#--

from   __future__  import unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

from   _TFL._Meta.Property        import Lazy_Property
from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.Object
import _TFL.Caller
import _TFL.Filter
import _TFL.Q_Exp

P = TFL.Attr_Query ()

def ddict (* ds) :
    result = {}
    for d in ds :
        result.update (d)
    return result
# end def ddict

class P_dict (TFL.Q_Exp.Q_Root) :
    """Parameter dict: supports lazy evaluation of dict arguments."""

    def __init__ (self, * args, ** kw) :
        self.args = args
        self.kw   = kw
    # end def __init__

    def __call__ (self, P) :
        result = {}
        Q_Root = TFL.Q_Exp.Q_Root
        for a in self.args :
            if isinstance (a, Q_Root) :
                a = a (P)
            result.update (a)
        for k, v in self.kw.iteritems () :
            if isinstance (v, Q_Root) :
                v = v (P)
            result [k] = v
        return result
    # end def __call__

# end class P_dict

class M_Definition (TFL.Meta.Object.__class__) :
    """Meta class for `Definition`."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        bn = tuple (reversed ([getattr (b, "_nested_", {}) for b in bases]))
        cls._nested_ = _nested_ = ddict (* bn)
        Q_Root = TFL.Q_Exp.Q_Root
        for k, v in dct.iteritems () :
            if isinstance (v, Q_Root) :
                setattr (cls, k, Lazy_Property (k, v))
            elif isinstance (v, M_Definition) :
                _nested_ [k] = v
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        for k, v in cls._nested_.iteritems () :
            setattr (result, k, v (R = result))
        return result
    # end def __call__

# end class M_Definition

class Definition (TFL.Meta.Object) :
    """Definition of parameters for media, i.e., CSS and JS, fragments.

    >>> class Defaults (Definition) :
    ...   foo = 1
    ...   bar = P.foo * 2
    ...   class nav_col (Definition) :
    ...     bar = 42
    ...     baz = 0
    ...     class own_links (Definition) :
    ...       qux = P.R.bar * 2
    ...       quy = P.T.bar * 2
    ...       quz = P.T.foo * 0.5
    ...     spec = P_dict (a = P.bar, border = "solid")
    ...
    >>> class App (Defaults) :
    ...   foo = 2
    ...   class nav_col (Defaults.nav_col) :
    ...     bar = 137
    ...
    >>> D = Defaults ()
    >>> E = App ()
    >>> D.foo, E.foo
    (1, 2)
    >>> D.bar, E.bar
    (2, 4)
    >>> D.nav_col.own_links.qux, E.nav_col.own_links.qux
    (84, 274)
    >>> D.nav_col.own_links.quy, E.nav_col.own_links.quy
    (4, 8)
    >>> D.nav_col.own_links.quz, E.nav_col.own_links.quz
    (0.5, 1.0)
    >>> sorted (D.nav_col.spec.items ()), sorted (E.nav_col.spec.items ())
    ([('a', 42), ('border', u'solid')], [('a', 137), ('border', u'solid')])
    """

    __metaclass__ = M_Definition

    def __init__ (self, R = None) :
        self.R = R
    # end def __init__

    @Once_Property
    def T (self) :
        R = self.R
        if R is not None :
            return R.T
        else :
            return self
    # end def T

# end class Definition

class _Parameters_Scope_ (TFL.Caller.Object_Scope_Mutable) :
    """Encapsulate media parameters so that it is usable as context for
       `exec` of a file containing media fragments.
    """

    _real_name = "Scope"

    class _Media_ (TFL.Meta.Object) :
        """Wrapper for media class"""

        def __init__ (self, cls, ext = None) :
            self._cls = cls
            self._    = self
            self._ext = ext if ext is not None else []
        # end def __init__

        def __call__ (self, * args, ** kw) :
            result = self._cls (* args, ** kw)
            self._ext.append (result)
            return result
        # end def __call__

        def __getattr__ (self, name) :
            return getattr (self._cls, name)
        # end def __getattr__

    # end class _Media_

    css_links            = property (lambda s : s.CSS_Link._ext)
    js_on_ready          = property (lambda s : s.JS_On_Ready._ext)
    rel_links            = property (lambda s : s.Rel_Link._ext)
    scripts              = property (lambda s : s.Script._ext)
    script_files         = property (lambda s : s.Script_File._ext)
    style_sheets         = property (lambda s : s.Style_Sheet._ext)

    def __init__ (self, parameters, env = None) :
        from _GTW._CSS  import import_CSS
        from _GTW.Media import CSS_Link, JS_On_Ready, Rel_Link, Script
        self.P                = parameters
        self.CSS_Link         = self._Media_ (CSS_Link)
        self.JS_On_Ready      = self._Media_ (JS_On_Ready)
        self.Rel_Link         = self._Media_ (Rel_Link)
        self.Script           = self._Media_ (Script)
        self.Script_File      = self._Media_ (import_CSS.Style_File)
        self.Style_Sheet = SS = self._Media_ (import_CSS.Style_Sheet)
        self.Style_File       = self._Media_ (import_CSS.Style_File, SS._ext)
        self.env              = env
        self.__super.__init__ \
            ( object = import_CSS
            , locls  = dict (Include = self.Include)
            )
    # end def __init__

    def Eval (self, * fragments) :
        self.globs = {}
        for f in fragments :
            self._eval_file (f)
        return self
    # end def Eval

    def _eval_file (self, filename) :
        with open (filename, "rt") as file :
            self.globs ["__name__"] = filename
            exec (file, self.globs, self)
    # end def _eval_file

    def Include (self, * includes, ** kw) :
        ignore_missing = kw.pop ("ignore_missing", False)
        assert not kw, kw
        env            = self.env
        get_source     = env.loader.get_source
        for fn in includes :
            if not fn.endswith (".media") :
                fn = "%s.media" % (fn, )
            source, path, _ = get_source (env, fn)
            self._eval_file              (path)
    # end def Include

    def __getitem__ (self, index) :
        try :
            if isinstance (index, basestring) and not index.startswith ("_") :
                return getattr (self, index)
        except AttributeError :
            return self.__super.__getitem__ (index)
    # end def __getitem__

Scope = _Parameters_Scope_ # end class

import os

__doc__ = r"""
>>> from _JNJ.Media_Defaults import Media_Defaults
>>> from _JNJ.Environment    import HTML
>>> base_dir        = os.path.abspath \
...    (os.path.join (os.path.dirname (__file__), "..", "_GTW", "__test__"))
>>> env             = HTML (load_path = base_dir)
>>> base_media      = os.path.join (base_dir, "_test.media")
>>> def as_string (fragments) :
...     return "\n\n".join \
...                ( str (s) for s in
...                    sorted (fragments, key = TFL.Getter.rank)
...                )

>>> scope = Scope (Media_Defaults, env).Eval (base_media)
>>> print as_string (scope.style_sheets)
a, abbr, acronym, address, article, aside, audio
  { border         : 0
  ; font           : inherit
  ; font-size      : 100%
  ; margin         : 0
  ; outline        : 0
  ; padding        : 0
  ; vertical-align : baseline
  }
<BLANKLINE>
/* --> rules from a existing CSS file `/
a.hide
{
    display:          none
}
/* <-- */
>>> print as_string (scope.script_files)
/* a test javascript file directly included */

>>> scope.scripts
[/media/GTW/js/jquery-1.5.2.min.js: text/javascript]
>>> scope.css_links
[all: /media/GTW/css/jquery.gritter.css]
>>> scope.rel_links
[href="/media/GTW/css/jquery.gritter.rel.css"]
>>> print as_string (scope.js_on_ready)
/* this is a JS on ready code */
"""
if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.Parameters
