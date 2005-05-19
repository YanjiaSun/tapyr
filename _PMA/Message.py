# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    Message
#
# Purpose
#    Model a mail message
#
# Revision Dates
#     3-Sep-2004 (CT) Creation
#     4-Sep-2004 (CT) Creation continued
#     6-Sep-2004 (CT) `Ascii.sanitized_filename` used in `_filename`
#    12-Sep-2004 (CT) s/ignore/replace/ in `decode` calls
#    12-Sep-2004 (CT) `_decoded_header` simplified and made more robust by
#                     passing `replace` to `decode`
#    12-Sep-2004 (CT) Exception handler added to `Message.summary` to avoid
#                     spam mails to raise `LookupError` on `decode`
#    12-Sep-2004 (CT) Exception handler added to `Message._time`
#                     (Man, do I hate spammers)
#    15-Sep-2004 (CT) Creation continued....
#    17-Nov-2004 (CT) `main` added
#    26-Nov-2004 (CT) `_formatted_body` changed to apply `.rstrip ("\r")` to
#                     each line yielded
#    26-Nov-2004 (CT) `message_from_file` factored
#    30-Nov-2004 (CT) `Message._get_header` robustified
#     3-Jan-2005 (CT) `_Message_._setup_body` robustified
#     4-Jan-2005 (CT) `Msg_Status` used
#     6-Jan-2005 (CT) `all_parts` added
#     6-Jan-2005 (CT) `formatted` changed to only `show_sep` if there is more
#                     than one part
#     6-Jan-2005 (CT) Argument `show_sep` added to `_formatted_part`
#     6-Jan-2005 (CT) `_setup_body` changed to handle `message/rfc822`
#                     correctly
#     6-Jan-2005 (CT) `Message.__init__` changed to pass `name` instead of
#                     `""` to `__super.__init__`
#     6-Jan-2005 (CT) `Message.__repr__` robustified
#    28-Mar-2005 (CT) `_formatted_body` changed to handle `text/x-*`
#                     mime-types better
#    28-Mar-2005 (CT) Redundant definition of `all_parts` removed from
#                     `Message`
#    28-Mar-2005 (CT) `_Msg_Part_` factored and `part_iter` added
#    29-Mar-2005 (CT) `formatted` changed to use `part_iter`
#    31-Mar-2005 (CT) `__str__` and `__repr__` factored up into `_Msg_Part_`
#    31-Mar-2005 (CT) `Body_Part` changed to use a `name` passed by caller
#                     and map `type` to `content_type` as supplied by `email`
#    31-Mar-2005 (CT) `Header_Part` changed to use `X-PMA-Headers` as `type`
#    18-May-2005 (CT) s/Header_Part/Message_Header/
#    18-May-2005 (CT) s/Body_Part/Message_Body/
#    18-May-2005 (CT) `_setup_body` changed to but `Message_Body` into `parts`
#    18-May-2005 (CT) `_formatted_headers` changed to yield `name` and
#                     formatted header line
#    18-May-2005 (CT) `more_body_lines` added to `Message_Header` and
#                     separate `Message_Header` instance for `more headers`
#                     removed
#    18-May-2005 (CT) `email_summary` (and `_date`, `_sender`, and `_time`)
#                     factored up
#    18-May-2005 (CT) `Part_Header` factored
#    19-May-2005 (CT) s/_charset/_get_charset/
#    19-May-2005 (CT) `_get_content_type` added and redefined for
#                     `Message_Body` to deal with broken `content-type`
#    19-May-2005 (CT) `part_iter` refactored (got rid of `if isinstance` and
#                     `_Pseudo_Part_`)
#    19-May-2005 (CT) Result of `_temp_body` cached
#    19-May-2005 (CT) `Message_MPA` added and `_Message_._setup_body` changed
#                     to call it for "multipart/alternative"
#    19-May-2005 (CT) `all_parts` removed
#    19-May-2005 (CT) Property for `subject` added
#    ��revision-date�����
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Mailcap
import _PMA.Msg_Status
import _TFL.Ascii
import _TFL.Filename
import _TFL._Meta.M_Class
import _TFL._Meta.Property

from   _TFL.predicate          import dict_from_list
from   _TFL.Regexp             import *

import sos
import time

_ws_pat = Regexp    (r"\s+")
now     = time.time ()

class _Msg_Part_ (object) :

    __metaclass__    = TFL.Meta.M_Class_SWRP

    __properties     = \
        ( TFL.Meta.Lazy_Property ("charset",  lambda s : s._get_charset ())
        , TFL.Meta.Lazy_Property
            ("content_type", lambda s : s._get_content_type ())
        , TFL.Meta.Lazy_Property ("filename", lambda s : s._filename ())
        , TFL.Meta.Lazy_Property \
            ("subject",  lambda s : self._decoded_header (email ["subject"]))
        , TFL.Meta.Lazy_Property ("type",     lambda s : s.content_type)
        )

    label_width      = 8
    number           = None
    summary_format   = "%(name)-10s %(type)-20s %(filename)s"
    _charset         = None
    _tfn             = None

    def __init__ (self, email, name) :
        self.email = email
        self.name  = name
        self.path  = None
        self.body  = None
        self.parts = []
        self._setup_body (email)
    # end def __init__

    def email_summary (self, email, format = None) :
        name  = self.name
        type  = self.content_type
        if format is None :
            format = self.summary_format
        number     = self.number
        if number is None :
            number = u""
        date       = self._date   (email) or u""
        sender     = self._sender (email) or u""
        subject    = self.subject
        if "%(body)" in format :
            _pl = email
            while _pl.is_multipart () :
                _pl = _pl.get_payload (0)
            body = _pl.get_payload (decode = True) or u""
            if isinstance (body, str) :
                try :
                    body = body.decode (self.charset, "replace")
                       ### XXX some emails trigger
                       ### `UnicodeDecodeError: 'ascii' codec can't decode
                       ### byte 0xe4` without `replace` argument
                except LookupError :
                    body = body.decode ("us-ascii", "replace")
            body = _ws_pat.sub (u" ", body.strip ()) or u"<empty>"
        return format % locals ()
    # end def email_summary

    def part_iter (self) :
        for p in self.parts :
            yield p
    # end def part_iter

    def summary (self, summary_format = None) :
        if summary_format is None :
            summary_format = self.summary_format
        return summary_format % dict \
            (name = self.name, type = self.type, filename = self.filename)
    # end def summary

    def _date (self, email, treshold = 86400 * 270) :
        t = self._time (email)
        if t :
            if now - t > treshold :
                format = "%d-%b  %Y"
            else :
                format = "%d-%b %H:%M"
            return time.strftime (format, time.localtime (t))
    # end def _date

    def _decoded_header (self, header) :
        result = []
        if header :
            for p, c in Lib.decode_header (header) :
                result.append (p.decode (c or "us-ascii", "replace"))
        result = u" ".join (result)
        return result
    # end def _decoded_header

    def _filename (self) :
        email  = self.email
        if email :
            result = email.get_param \
                ("filename", header = "Content-Disposition")
            if not result :
                result = email.get_param ("name")
            if isinstance (result, tuple) :
                result = unicode (result [2], result [0] or "us-ascii")
            return TFL.Ascii.sanitized_filename (self._decoded_header (result))
    # end def _filename

    def _formatted_headers (self, headers = None) :
        email = self.email
        for n in (headers or self.headers_to_show) :
            n, h = self._get_header (email, n)
            if h :
                yield n, "%-*s: %s" % \
                    (self.label_width, n, self._decoded_header (h))
    # end def _formatted_headers

    def _get_charset (self) :
        result = self._charset
        if result is None :
            email = self.email
            if email :
                result = email.get_charset ()
                if result is None :
                    result = email.get_param ("charset", "us-ascii")
        return result
    # end def _get_charset

    def _get_content_type (self) :
        return self.email.get_content_type ().lower ()
    # end def _get_content_type

    def _get_header (self, email, name) :
        if isinstance (name, tuple) :
            for n in name :
                result = email [n]
                if result is not None :
                    name = n
                    break
            else :
                name = ""
        else :
            result = email [name]
        return name.capitalize (), result
    # end def _get_header

    def _sender (self, email) :
        sender = \
            (  email ["from"]
            or email ["reply-to"]
            or email ["return-path"]
            or email.get_unixfrom ()
            )
        if sender :
            sender = \
                (  filter (None, Lib.getaddresses ((sender, )) [0])
                or (None, )
                ) [0]
            return self._decoded_header (sender)
    # end def _sender

    def _separators (self, sep_length) :
        yield ""
        yield ( "%s part %s %s" % ("-" * 4, self.name, "-" * sep_length)
              ) [:sep_length]
    # end def _separators

    def _temp_body (self) :
        if self._tfn is None or not sos.path.isfile (self._tfn) :
            result = TFL.Filename \
                ( sos.tempfile_name ()
                , (self.filename or "").encode ("us-ascii", "ignore")
                ).name
            f = open (result, "w")
            try :
                f.write (self.body)
            finally :
                f.close ()
            self._tfn = result
        return self._tfn
    # end def _temp_body

    def _time (self, email) :
        for date in email ["date"], email ["delivery-date"] :
            if date :
                parsed = Lib.parsedate_tz (date)
                if parsed is not None :
                    try :
                        return Lib.mktime_tz (parsed)
                    except (OverflowError, ValueError) :
                        pass
    # end def _time

    def __str__ (self) :
        return self.summary_format % dict \
            (name = self.name, type = self.type, filename = self.filename)
    # end def __str__

    def __repr__ (self) :
        return "%s %s : %s" % (self.__class__.__name__, self.name, self.type)
    # end def __repr__

# end class _Msg_Part_

class Message_Body (_Msg_Part_) :
    """Model the body of a (non multi-part) message or message-part"""

    _file_result_pattern = Regexp \
        ( r"[^:]+ \s* : \s* (?P<type> [^;]+) "
          r"(?: \s* ; \s* charset=(?P<charset> [-A-Za-z0-9]+))?"
        , re.VERBOSE
        )

    def __init__ (self, email, name, headers_to_show) :
        assert not email.is_multipart ()
        self.headers_to_show = headers_to_show
        self.lines           = None
        self.__super.__init__ (email, name)
    # end def __init__

    def body_lines (self, sep_length = 79) :
        lines = self.lines
        if lines is None :
            if self.body :
                type = self.content_type
                if type == "text/plain" or type.startswith ("text/x-") :
                    lines = self.body.split ("\n")
                    ### XXX put full-quotes-at-end into `self.parts [0]`
                else :
                    cap = PMA.Mailcap [type]
                    if cap :
                        lines = cap.as_text (self._temp_body ())
                    if lines is None and type.startswith ("text/") :
                        lines = self.body.split ("\n")
                if lines is not None :
                    self.lines = lines
        if lines is not None :
            charset = self.charset
            for l in lines :
                yield l.decode (charset, "replace").rstrip ("\r")
        else :
            hp = Part_Header (self.email, self.headers_to_show)
            self.lines = lines = list (hp.formatted (sep_length))
            for l in lines :
                yield l
    # end def body_lines

    formatted = _formatted = body_lines

    def _get_content_type (self) :
        result = self.__super._get_content_type ()
        if result == "application/octet-stream" :
            pipe = sos.popen     ("file -i %s" % (self._temp_body (), ), "r")
            f_result = pipe.read ()
            pipe.close           ()
            pat = self._file_result_pattern
            if pat.match (f_result) :
                result = pat.type
                if pat.charset :
                    self._charset = pat.charset
        elif result == "application/python" :
            if self.filename.endswith (".py") :
                result = "text/x-python"
        return result
    # end def _get_content_type

    def _separators (self, sep_length) :
        if self.name == "Body" :
            seps = ("", "-" * sep_length, "")
        else :
            seps = self.__super._separators (sep_length)
        for s in seps :
            yield s
    # end def _separators

    def _setup_body (self, email) :
        payload = email.get_payload (decode = True)
        if payload :
            self.body = payload.strip ()
    # end def _setup_body

# end class Message_Body

class Part_Header (_Msg_Part_) :
    """Model the headers of a message part as pseudo-part"""

    __properties     = \
        ( TFL.Meta.Lazy_Property ("type", lambda s : "x-pma/part-headers")
        ,
        )

    def __init__ (self, email, headers_to_show) :
        self.headers_to_show = headers_to_show
        self.__super.__init__ (email, "Headers")
    # end def __init__

    def body_lines (self, sep_length = 79) :
        return self._fh
    # end def body_lines

    formatted = _formatted = body_lines

    def more_body_lines (self, sep_length = 79) :
        return self._mh
    # end def more_body_lines

    def _separators (self, sep_length) :
        return ()
    # end def _separators

    def _setup_body (self, email) :
        self._fh  = _fh = []
        add       = _fh.append
        _hn       = {}
        for n, h in self._formatted_headers (self.headers_to_show) :
            add (h)
            _hn [n] = h
        self.body = "\n".join (_fh)
        mhn       = sorted ([k for k in email.keys () if k not in _hn])
        self._mh  = []
        add       = self._mh.append
        seen      = {}
        for n, h in self._formatted_headers (mhn) :
            if not h in seen :
                add  (h)
                seen [h] = True
    # end def _setup_body

# end class Part_Header

class Message_Header (Part_Header) :
    """Model the headers of an email as pseudo-part"""

    __properties     = \
        ( TFL.Meta.Lazy_Property ("type", lambda s : "x-pma/headers")
        ,
        )

    def __init__ (self, email, headers_to_show, summary) :
        self.summary_line = summary
        self.__super.__init__ (email, headers_to_show)
    # end def __init__

# end class Message_Header

class _Message_ (_Msg_Part_) :

    def body_lines (self, sep_length = 79) :
        return ()
    # end def body_lines

    def formatted (self, sep_length = 79) :
        for p in self.part_iter () :
            for l in p.formatted (sep_length) :
                yield l
    # end def formatted

    _formatted = formatted

    def _new_part (self, name, p, i) :
        p_name = ".".join (filter (None, (name, str (i))))
        if p.is_multipart () :
            result = Message_Part (p, p_name)
        else :
            result = Message_Body (p, p_name, Message_Part.headers_to_show)
        return result
    # end def _new_part

    def _setup_body (self, email) :
        name       = b_name = self.name
        self.parts = parts  = []
        self.body  = None
        if isinstance (self, Message) or not b_name :
            b_name = "Body"
        if email.is_multipart () :
            payload = email.get_payload ()
            type    = email.get_content_type ()
            if type == "message/rfc822" :
                p, = payload
                parts.append (Message (p, name))
            elif type == "multipart/alternative" and len (payload) > 1 :
                parts.append (Message_MPA (email, b_name, * payload))
            else :
                parts.extend \
                    ([   self._new_part (name, p, i+1)
                     for (i, p) in enumerate (payload)
                     ]
                    )
        else :
            b = Message_Body (email, b_name, self.headers_to_show)
            parts.append     (b)
    # end def _setup_body

# end class _Message_

class Message_MPA (_Message_) :
    """Model the parts of a multipart/alternative MIME message"""

    __properties     = \
        ( TFL.Meta.Lazy_Property ("type", lambda s : "x-pma/mpa")
        ,
        )

    def __init__ (self, email, name, head, * rest) :
        self.head = head
        self.rest = rest
        self.__super.__init__ (email, name)
    # end def __init__

    def _setup_body (self, email) :
        name       = self.name
        self.parts = [self._new_part (name, self.head, 1)]
        self.altp  = \
            [self._new_part (name, p, i+2) for (i, p) in enumerate (self.rest)]
    # end def _setup_body

# end class Message_MPA

class Message_Part (_Message_) :
    """Model a part of a multi-part MIME message"""

    headers_to_show  = ("content-type", "content-disposition")

# end class Message_Part

class Message (_Message_) :
    """Model a mail message"""

    headers_to_show  = \
        ( ("date", "delivery-date")
        , ("from", "reply-to", "return-path")
        , ("to", "envelope-to")
        , "cc"
        , "subject"
        )
    short_summary_format = unicode \
        ( "%(name)s %(date).12s %(sender).20s %(subject).45s "
        )
    summary_format   = unicode \
        ( "%(number)4s %(date)-12.12s %(sender)-20.20s %(subject)-25.25s "
          "[%(body)-50.50s"
        )

    date             = property (lambda s : s._date   (s.email))
    sender           = property (lambda s : s._sender (s.email))
    time             = property (lambda s : s._time   (s.email))

    def __init__ (self, email, name = None, mailbox = None, status = None, number = None) :
        if status is None :
            status = PMA.Msg_Status ()
        self.__super.__init__ (email, name)
        self.mailbox = mailbox
        self.status  = status
        self.number  = number
    # end def __init__

    def formatted (self, sep_length = 79) :
        self.status.set_read   ()
        for p in self.part_iter () :
            for s in p._separators (sep_length) :
                yield s
            for l in p._formatted  (sep_length) :
                yield l
    # end def formatted

    def part_iter (self) :
        email = self._reparsed ()
        yield Message_Header \
            ( email
            , self.headers_to_show
            , self.summary (self.short_summary_format)
            )
        for p in self.__super.part_iter () :
            yield p
    # end def part_iter

    def summary (self, format = None) :
        return self.email_summary (self.email, format)
    # end def summary

    def _reparsed (self) :
        result = self.email
        if self.path and not result._pma_parsed_body :
            if self.mailbox :
                parser = self.mailbox.parser.parse
            else :
                parser = Lib.message_from_file
            fp = open (self.path, "r")
            try :
                result = self.email = parser (fp)
            finally :
                fp.close ()
            result._pma_dir         = getattr (self.email, "_pma_dir",  None)
            result._pma_path        = getattr (self.email, "_pma_path", None)
            result._pma_parsed_body = True
            self._setup_body (result)
        return result
    # end def _reparsed

    def __str__ (self) :
        return self.summary ()
    # end def __str__

    def __repr__ (self) :
        if self.mailbox :
            result = "%s %s:%s" % \
                (self.__class__.__name__, self.mailbox.path, self.name)
        else :
            result = "%s %s" % (self.__class__.__name__, self.name)
        return result
    # end def __repr__

# end class Message

def message_from_file (filename, parser = None) :
    if parser is None :
        parser = Lib.Parser ()
    fp = open (filename)
    try :
        email = parser.parse (fp)
    finally :
        fp.close ()
    return Message (email, sos.path.split (filename) [-1])
# end def message_from_file

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line \
        ( arg_spec    = ("message:S?Message to print")
        , option_spec =
            (
            )
        , description = "Print mail messages"
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    parser = Lib.Parser ()
    for m in cmd.argv :
        msg = message_from_file (m, parser)
        print u"\n".join (msg.formatted ()).encode ("iso-8859-15", "replace")
# end def main

"""
from   _PMA                    import PMA
import _PMA.Mailbox
mb=PMA.MH_Mailbox ("/swing/private/tanzer/MH/PMA")
print mb.summary ().encode ("iso-8859-1", "replace")
m = mb.messages [-1]
m._reparsed ()
def show (m, head = "") :
    for p in m.part_iter () :
        print head, type (p), p.name, p.type, id (p.email), p.email.is_multipart()
        show (p, head + " ")

show (m)
"""

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    main (command_spec ())
### __END__ PMA.Message
