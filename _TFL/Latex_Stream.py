# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2003 TTTech Computertechnik GmbH. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL/Latex_Stream
#
# Purpose
#    Comfortable output stream for a Latex source file
#
# Revision Dates
#    28-Jun-1999 (MG) Creation
#    10-Oct-2000 (RM) Added some methodes to the Latex_Stream and all the nice
#                     TeX wrappers.
#    23-Oct-2000 (RM) Added fnode and made other commands more robust
#    25-Oct-2000 (RM) Added constructor which calls file_header
#    26-Oct-2000 (RM) psframe must handle floats not only ints
#    27-Oct-2000 (RM) Automatic generation of most of the functions
#    31-Oct-2000 (RM) Added class Figure_
#    30-Jan-2001 (RMA) Changed to Environment.username
#    21-Sep-2001 (MG) `item` changed to use `fpul` instead of implementing
#                     the same functionally twice
#    21-Sep-2001 (MG) `begin_pspicture`: allow only on pair of borders.
#    21-Sep-2001 (RMA) Corrected _remove_white
#    26-Sep-2001 (MG) Moved into package `TFL`
#    26-Sep-2001 (MG) Call of `file_header` removed from
#                     `Latex_Stream.__init__`
#    26-Sep-2001 (MG) `*_document`, include, and `input` added
#    10-Jun-2002 (RMA) Short name support
#    11-Jun-2003 (CT)  s/== None/is None/
#    11-Jun-2003 (CT)  s/!= None/is not None/
#    14-Aug-2003 (RMA) Added paramter for begin_section
#    10-Oct-2003 (RMA) Various new methods
#     1-Dec-2003 (RMA) Fixed wrong comment char for file_header.
#     1-Dec-2003 (MG)  Fixed `file_header`: if no `comment_char` is
#                      specified, `comment_line_head` will be used
#     1-Dec-2003 (RMA) Factorized _begin_section
#     2-Dec-2003 (MG) `item`: parameter `item_indent_only` extended
#     9-Dec-2003 (RMA) Added define and cfunctiondesc
#    11-Dec-2003 (RMA) Added cmacrodesc.
#    23-Dec-2003 (RMA) Added sanatized_label
#    29-Dec-2003 (RMA) Added begin_block and end_block
#    05-Jan-2004 (RMA) Added itemize_txt
#    15-Jan-2004 (RMA) Improved define
#    20-Jan-2004 (RMA) Improved interface of begin_tabular
#    25-Jan-2004 (RMA) Improved end_tabular
#    25-Jan-2004 (RMA) Added begin/end_chapter
#    25-May-2004 (RMA) Fixed itemize_txt
#    15-Feb-2005 (MG)  Use `isinstance` instead of `type`
#    ««revision-date»»
#--

from    Formatted_Stream import Formatted_Stream
from    Regexp           import *
import  re
import  time
import  sys
import  sos
import  string
import  Environment

slash_pat = Regexp (r"[/\\]")

def sanatized_label (txt) :
    txt = slash_pat.sub ("", txt)
    return txt


item_head_pat   = Regexp (r"^\s*- ", re.MULTILINE)
item_tail_pat   = Regexp ( "(\n\n(?=[^- ])|$)")

def itemize_txt (description) :
    desc      = description
    d         = "\n".join (desc)
    start     = 0
    desc      = []
    while item_head_pat.search (d, start) :
        item_tail_pat.search (d, item_head_pat.end ())
        print item_head_pat.start ()
        desc.append (d [start : max (0, item_head_pat.start () - 1)])
        desc.append (r"\begin{itemize}")
        start = item_tail_pat.start ()
        items = "\n" + d [item_head_pat.start () : start]
        for item in filter (None, items.split ("\n- ")):
            item_txt = " ".join (item.split ("\n"), )
            if string.strip (item_txt) :
                desc.append (r"  \item %s" % item_txt)
        desc.append (r"\end{itemize}")
    desc.append (d [start : ])
    return desc



class Latex_Stream (Formatted_Stream) :
    """Formatted output stream fot a LaText source file."""

    __Ancestor        = Ancestor = Formatted_Stream

    comment_line_head = "%"
    comment_line_tail = ""

    def __init__ (self, file = None, indent_delta = 2, open_as = "w") :
        self.__Ancestor.__init__ (self, file, indent_delta, open_as)
    # end def __init__

    def file_header (self, filetype, toolname = None, comment_char = None) :
        if toolname is None :
            toolname = sys.argv [0]
        if comment_char is None :
            comment_char = self.comment_line_head
        user = " by user " + Environment.username
        self.fputl ( "%s %s"              % (comment_char, filetype)
                   , "%s generated by %s" % (comment_char, toolname)
                   , "%s written on %s%s"
                       % ( comment_char
                         , time.strftime ( "%a %d-%b-%Y %H:%M:%S"
                                         , time.localtime (time.time ())
                                         )
                         , user
                         )
                   )
        self.put_soft_line ()
    # end def file_header

    def _begin_section (self, level, name, attributes = "", insert_newline = 1) :
        """Begin of new section"""
        if not self.at_bol :
            self.putl ()
        self.putl   ("", r"\%s{%s}%s" % (level, name, attributes))
        if insert_newline :
            self.put_soft_line ()
        self.indent ()


    def begin_chapter (self, name, attributes = "", insert_newline = 1) :
        self._begin_section ("chapter", name, attributes, insert_newline)

    end_chapter = Formatted_Stream.deindent

    def begin_section (self, name, attributes = "", insert_newline = 1) :
        self._begin_section ("section", name, attributes, insert_newline)
    # end def begin_section

    end_section  = Formatted_Stream.deindent

    def begin_subsection (self, name, attributes = "", insert_newline = 1) :
        self._begin_section ("subsection", name, attributes, insert_newline)
    # end def begin_subsection

    end_subsection  = Formatted_Stream.deindent

    def begin_subsubsection (self, name, attributes = "", insert_newline = 1) :
        self._begin_section ("subsubsection", name, attributes, insert_newline)
    # end def begin_susubbsection

    end_subsubsection  = Formatted_Stream.deindent

    def _begin_block (self, name, attributes = "") :
        """Write the beginning `\begin {}' statement for a block-statement.
        """
        if not self.at_bol :
            self.putl ()
        self.putl (r"\begin{%s}%s" % (name, attributes))
        self.indent ()
    # end def _begin_block

    begin_block = _begin_block

    def _end_block (self, name, attributes = "") :
        """Write the end `\end {}' statement for a block-statement.
        """
        self.deindent ()
        self.putl     (r"\end{%s}%s" % (name, attributes))
        self.putsl    (1)
    # end def _begin_block

    end_block = _end_block

    def begin_description (self, environment = "description") :
        """Write the beginning of a description block."""
        self._begin_block (environment)
    # end def begin_description

    def end_description (self, environment = "description") :
        """Write the end of a description block"""
        self._end_block (environment)
    # end def end_description

    def begin_document (self) :
        self._begin_block ("document")
    # end def begin_document

    def end_document (self) :
        self._end_block ("document")
    # end def end_document

    def input (self, filename) :
        self.putl(r"\input{%s}" % filename)
    # end def input

    def include (self, filename) :
        self.putl(r"\include{%s}" % filename)
    # end def include

    def item (self, item_name, text, item_length = 0, item_indent_only = None) :
        """Write a `item' statement for a block structure to the stream."""
        if isinstance (text, string) :
            text = (text, )
        text = list (text)
        item = r"\item "
        if item_indent_only :
            text[0]   = "%s %s" % (item_name, text [0])
            item_name = item
        else :
            item_name = item + item_name + " "
        self.fputl (text, first_head = item_name, break_intend = item_length)
    # end def item

    def item_list (self, * name_text_pairs) :
        """"""
        item_len = 0
        for name, text in name_text_pairs :
            item_len = max (len (name), item_len)
        item_len = item_len + 1
        for name, text in name_text_pairs :
            self.item (name, text, item_len)
    # end def item_list

    def _caption_label (self, cap, label_, shortname) :
      if cap:
        self.putl (caption (cap, shortname))
      if label_:
        self.putl (label (label_))
    # end def _caption_label

    def begin_center (self) :
        self._begin_block ("center")
    # end def begin_center

    def end_center (self) :
        self._end_block ("center")
    # end def end_center

    def begin_picture (self, width = 0, height = 0) :
        attri = "(%f,%f)" % (width, height)
        self._begin_block ("picture", attri)
    # end def begin_picture

    def end_picture (self) :
        self._end_block ("picture")
    # end def end_picture

    def begin_pspicture (self, x1, y1, x2 = None, y2 = None) :
        attr  = []
        for x, y in (x1, y1), (x2, y2) :
            if (x is not None) and (y is not None) :
                attr.append ("(%f,%f)" % (x, y))
        attri = string.join (attr, "")
        self._begin_block ("pspicture", attri)
    # end def begin_pspicture

    def end_pspicture (self) :
        self._end_block ("pspicture")
    # end def end_pspicture

    def begin_figure (self, caption = None, label = None, shortlabel = None, position = "htp") :
        self._begin_block ("figure", "[%s]" % position)
        self._caption_label (caption, label, shortlabel)
    # end def begin_figure

    def end_figure (self, caption = None, label = None, shortlabel = None) :
        self._caption_label (caption, label, shortlabel)
        self._end_block ("figure")
    # end def end_figure

    def h_line (self):
        self.putl (r"\hline")

    def begin_landscape (self) :
        self._begin_block ("landscape")

    def end_landscape (self) :
        self._end_block ("landscape")


    def _tab_marker (self, longtable) :
        tab_marker = "tabular"
        if longtable :
            tab_marker = "longtable"
        return tab_marker

    def begin_table (self, placement = "htbp")  :
        self._begin_block ("table", "[%s]" % placement)
    # end def begin_table


    def end_table (self, caption, label) :
        self.putl (r"\caption{%s}" % caption)
        self.putl (r"\label{%s}" % sanatized_label (label))
        self._end_block ("table")
    # end def end_table

    def begin_tabular (self, widths = None, tablespecs = None, headers = None, percentage = 0, **kw):
        colsep      = kw.get ("colsep",     "|")
        longtable   = kw.get ("longtable",  "0")
        endfoot     = kw.get ("endfoot",     None)
        endlastfoot = kw.get ("endlastfoot", None)

        self.putw \
            ("\\begin{%s}[t]{%s" % (self._tab_marker (longtable), colsep))
        if widths :
            self.columns = len (widths)
            if percentage :
                widths  = map (lambda x: "%f\\linewidth" % x , widths)
            else :
                widths  = map (lambda x: "%fcm" % x , widths)

            for w in widths :
                self.putw ("p{%s}%s" % (w, colsep))
        elif tablespecs :
            self.columns = len (tablespecs)
            for w in tablespecs :
                self.putw ("%s%s" % (w, colsep))
        else :
            assert (0) # Neither widths nor tablespecs provided

        self.putl ("}")
        self.h_line ()
        if headers:
            entries = map (lambda x: textbf (x), headers)
            self.tabular_entry (entries)
            self.h_line ()
            self.h_line ()
            self.putl (r"\endhead")
        if endfoot:     self.putl (endfoot,     r"\endfoot")
        if endlastfoot: self.putl (endlastfoot, r"\endlastfoot")
        self.indent ()
    # end __init__

    def tabular_entry (self, entries, format_fn = None) :
        if (len (entries) <> self.columns) :
            print "len (entries): %d" % len (entries)
            print "self.columns:  %d" % self.columns
            assert (len (entries) == self.columns)

        if format_fn :
            new_entries = []
            column = 0

            for e in entries :
                if format_fn :
                    new_e = format_fn (self, column, e)
                new_entries.append (new_e)
                column += 1
            entries = new_entries

        self.putw (string.join (entries, " & "))
        self.putl (" \\CR")
        self.h_line ()
    # end def tabular_entry

    def end_tabular (self, longtable = 0, **kw):
        caption     = kw.get ("caption",     None)
        label       = kw.get ("label",       None)
        shortname   = kw.get ("shortname",       None)

        self._caption_label (caption, label, shortname)
        self.deindent ()
        self.putl (r"\end{%s}" % self._tab_marker (longtable))
    # end def end_tabular

    def define (self, name, code, eol_comment = "", params = 0) :
        param_txt = "/"
        if params :
            _params   = ["#%i" % (i + 1) for i in range (params)]
            param_txt = string.join (_params, "")
        self.putw   (r"\def\%s%s{%s}"
                    % (name, param_txt, code)
                    )
        if eol_comment :
            self.putw ("%%")
        self.putl     ()


    def _cfunc (self, macro, ret_type, name, params, ret_desc = None) :
        environment = ("cfuncdesc", "cmacrodesc") [macro]
        self.putsl           (1)
        self.putl            (r"\begin{%s}" % environment)
        self.indent          ()
        if ret_desc :
            self.putl        (r"[%s]" % ret_desc)
        self.putl            (r"{%s}" % ret_type)
        self.putl            (r"{%s}" % name)
        self.putl            (r"{%s}" % params)
        self.putl            ("")

    def begin_cfuncdesc (self, ret_type, name, params, ret_desc = None) :
        self._cfunc (0, ret_type, name, params, ret_desc)

    def begin_cmacrodesc (self, ret_type, name, params, ret_desc = None) :
        self._cfunc (1, ret_type, name, params, ret_desc)

    def end_cfuncdesc (self) :
        self._end_block ("cfuncdesc")

    def end_cmacrodesc (self) :
        self._end_block ("cmacrodesc")


# end class Latex_Stream

#----------------------------------------------------------------------
class Figure_ :

    def __init__ (self, name, outdir = "auto", prefix = "") :
        self.name   = name
        filename    = string.replace (string.lower (name), " ", "_")
        filename    = sos.path.join (outdir, prefix + filename)
        self.stream = Latex_Stream (filename + ".tex")

        self.preamble     (self.name)
        self.picture      ()
        self.epilog       (self.name)
        self.stream.close ()
    # end def __init__

    def _remove_white (self, s) :
        return filter (lambda c : c not in string.whitespace, s)
    # end def _remove_white

    def preamble (self, graphic_name) :
        self.stream.begin_figure ()
        self.stream.putl         (r"\setlength{\unitlength}{1cm}")
        self.stream.begin_center ()
    # end def preamble

    def epilog (self, graphic_name) :
        file = self.stream
        label  = "fig:" + self._remove_white (graphic_name)
        file.end_center ()
        file.end_figure (graphic_name, label)
    # end def epilog

# end class Figure_

#----------------------------------------------------------------------

class Dir_Node :
    """ Class for making directory trees with PsTricks.
        Simple instaniate nodes and add children with add.

        root = Dir_Node ("C:")
        root.add (Dir_Node ("Programme"))

        It also features empty -- no names -- nodes which are usefull
        as collections.
    """

    indent    = 1
    vertical  = 0.4
    options   = None
    factor    = 2.0/4

    __id      = 0


    #----------------------------------------------------------------------

    def __init__ (self, name = None) :
        self.name = name
        self.children = []
        self.identifier = "%s" % self._new_id ()
    # end def __init__

    def add (self, *children) :
        for child in children :
          self.children.append (child)
        return self
    # end def add

    def write (self, file, x = 0, y = 0) :
        return self._rec_write (file, x, y)
    # end def write

    #----------------------------------------------------------------------

    def _new_id (self) :
        Dir_Node.__id = Dir_Node.__id + 1
        return Dir_Node.__id
    # end def _new_id

    def _node_label (self, x, y, identifier) :
        return "%d%d%s" % (x, y, identifier)
    # end def _node_label

    def _rec_write (self, file, x = 0, y = 0) :
        _y = y

        if self.name:
            file.putl ("%")
            file.putl (pnode ( x + (1 - self.factor) * self.indent
                             , y - 0.2, self.identifier + "_D"
                             )
                      )
            file.putl (pnode (x, y, self.identifier + "_"))
            file.putl (uput (0, x, y, self.name))

            nodelabel = self._node_label (x - self.indent, y, self.identifier)
            file.putl ( ncline ( "-"
                               , nodelabel
                               , self.identifier + "_", self.options
                               )
                      )
            x = x + self.indent
        else :
            file.putl (pnode ( x - self.factor * self.indent, y
                             , self.identifier + "_D"
                             )
                      )
            y = y + self.vertical

        nodelabel = None

        for child in self.children :
            file.indent ()

            y = y - self.vertical

            nodelabel = self._node_label (x - self.indent, y, child.identifier)
            file.putl (pnode (x - self.factor*self.indent, y, nodelabel))
            y = y + child._rec_write (file, x, y)

            file.deindent ()
            file.put_soft_line ()

        if nodelabel:
            file.putl (ncline ("-", self.identifier + "_D", nodelabel))

        return y - _y
    # end def _rec_write

#end class Dir_Node



#----------------------------------------------------------------------

def vspace (length, unit = "cm") :
    return r"\vspace{%f%s}" % (length, unit)


def pnode (x, y, label) :
    return r"\pnode(%f,%f){%s}" % (x, y, label)

def rput (x, y, text) :
    return r"\rput(%f,%f){%s}" % (x, y, text)

def psframe (x1, y1, x2, y2, options = None) :
    s = r"\psframe"
    if options :
      s = s + "[" + options + "]"
    return s + "(%f,%f)(%f,%f)" % (x1,  y1,  x2, y2)

def fnode (x, y, name, width = None, height = None) :
    param = ""
    if width :
        param = param + "framesize=%s" % width
        if height :
            param = param + " %s" % height

    if param :
        param = "[" + param + "]"

    return r"\fnode%s(%f,%f){%s}" % (param, x, y, name)


def latex_cmd (name, options, *args) :
    cmd = r"\%s" % name
    if options :
        cmd = cmd + "[" + options + "]"
    for arg in args:
        cmd = cmd + "{" + "%s" % arg + "}"
    return cmd


#----------------------------------------------------------------------


def psset (name, value) :
    return r"\psset{%s=%s}" % (name, value)

def uput (angle, x, y, text) :
    return r"\uput[%s](%f,%f){%s}" % (angle, x, y, text)

#----------------------------------------------------------------------


_commands0          = [ "clearpage", "smallskip" ]


# Commands with one parameter
_commands1          = [ "textsf", "texttt", "textbf", "centering"
                      , "tiny",   "footnotesize", "small", "smaller"
                      , "label",  "caption"
                      , "rotateleft", "psovalbox", "psframebox"
                      , "thput", "tvput"
                      , "naput", "ncput", "nbput"
                      ]
# Command with two parameters
_commands2          = [ "parbox"
                      , "rnode", "Rnode"
                      ]

# Command with three parameters
_commands3          = [ "ncangles", "ncarc", "ncloop", "ncline"
                      ]

#----------------------------------------------------------------------
for c in _commands0 :
  s = "def %s () : " \
      "  return \"\\%s\"" % (c, c)
  exec (s)


for c in _commands1 :
  s = "def %s (p, options = None) : " \
      "  return latex_cmd (\"%s\", options, p)" % (c, c)
  exec (s)

for c in _commands2 :
  s = "def %s (p1, p2, options = None) :" \
      "  return latex_cmd (\"%s\", options, p1, p2)" % (c, c)
  exec (s)


for c in _commands3 :
  s = "def %s (p1, p2, p3, options = None) :" \
      "  return latex_cmd (\"%s\", options, p1, p2, p3)" % (c, c)
  exec (s)

### __END__ TFL/Latex_Stream
from _TFL import TFL
TFL._Export ("*")
