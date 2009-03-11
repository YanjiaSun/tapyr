# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Currency
#
# Purpose
#    Model a currency
#
# Revision Dates
#     7-Mar-2009 (CT) Creation
#    ��revision-date�����
#--

from   _TFL import TFL

import _TFL._Meta.Object
import _TFL.Decorator

import decimal
import re

### see Fri97, p.229, p.292
sep_1000_pat   = re.compile ("(\d{1,3}) (?= (?: \d\d\d)+ (?! \d) )", re.X)
comma_dec_pat  = re.compile ("([0-9.]+) , (\d{2})$",                 re.X)
period_dec_pat = re.compile ("([0-9,]+) \. (\d{2})$",                re.X)

@TFL.Decorator
def _binary_operator (f) :
    def _ (self, rhs) :
        C_Type = self.C_Type
        if isinstance (rhs, C_Type) :
            rhs = rhs.amount
        return f (self, rhs)
    return _
# end def _binary_operator

@TFL.Decorator
def _binary_operator_currency (f) :
    def _ (self, rhs) :
        C_Type = self.C_Type
        if isinstance (rhs, C_Type) :
            rhs = rhs.amount
        return C_Type (f (self, rhs))
    return _
# end def _binary_operator

@TFL.Decorator
def _binary_operator_inplace (f) :
    def _ (self, rhs) :
        C_Type = self.C_Type
        if isinstance (rhs, C_Type) :
            rhs = rhs.amount
        f (self, rhs)
        self.amount = self.normalized_amount (self.amount)
        return self
    return _
# end def _binary_operator

class _Currency_ (TFL.Meta.Object) :

    name            = "EUR"
    sloppy_name     = "EUR"
    symbol          = property (lambda s : s._symbol or s.sloppy_name)

    decimal_sign    = "."
    sep_1000        = ","

    C_Type          = property (lambda s : s.__class__)
    _currency       = property (lambda s : s.amount)
    _symbol         = None

    def as_string_s (self, round = 0) :
        result = self.as_string   (round)
        result = sep_1000_pat.sub (r"\g<1>%s" % self.sep_1000, result)
        return result
    # end def as_string_s

    ### binary operators

    @_binary_operator_currency
    def __add__ (self, rhs) :
        return self.amount + rhs
    # end def __add__

    __radd__ = __add__

    @_binary_operator_currency
    def __sub__ (self, rhs) :
        return self.amount - rhs
    # end def __sub__

    __rsub__ = __sub__

    @_binary_operator_currency
    def __mul__ (self, rhs) :
        return self.amount * rhs
    # end def __mul__

    __rmul__ = __mul__

    @_binary_operator_currency
    def __div__ (self, rhs) :
        return self.amount / rhs
    # end def __div__

    __rdiv__ = __div__

    @_binary_operator_currency
    def __floordiv__ (self, rhs) :
        return self.amount // rhs
    # end def __floordiv__

    __rfloordiv__ = __floordiv__

    @_binary_operator_currency
    def __mod__ (self, rhs) :
        return self.amount % rhs
    # end def __mod__

    __rmod__ = __mod__

    @_binary_operator
    def __divmod__ (self, rhs) :
        return tuple (self.C_Type (x) for x in divmod (self.amount, rhs))
    # end def __divmod__

    __rdivmod__ = __divmod__

    ### binary operators in-place (aka, augmented assignment operators)

    @_binary_operator_inplace
    def __iadd__ (self, rhs) :
        self.amount += rhs
    # end def __iadd__

    @_binary_operator_inplace
    def __isub__ (self, rhs) :
        self.amount -= rhs
    # end def __isub__

    @_binary_operator_inplace
    def __imul__ (self, rhs) :
        self.amount *= rhs
    # end def __imul__

    @_binary_operator_inplace
    def __idiv__ (self, rhs) :
        self.amount /= rhs
    # end def __idiv__

    @_binary_operator_inplace
    def __ifloordiv__ (self, rhs) :
        self.amount //= rhs
    # end def __ifloordiv__

    ### unary operators

    def __abs__ (self) :
        return self.C_Type (abs (self.amount))
    # end def __abs__

    def __float__ (self) :
        return float (self.amount)
    # end def __float__

    def __int__ (self) :
        return int (self.amount)
    # end def __int__

    def __neg__ (self) :
        return self.C_Type (- self.amount)
    # end def __neg__

    def __nonzero__ (self) :
        return bool (self.amount)
    # end def __nonzero__

    def __pos__ (self) :
        return self.C_Type (self.amount)
    # end def __pos__

    ### comparison operators

    @_binary_operator
    def __eq__ (self, rhs) :
        return self.amount == rhs
    # end def __eq__

    @_binary_operator
    def __ne__ (self, rhs) :
        return self.amount != rhs
    # end def __ne__

    @_binary_operator
    def __ge__ (self, rhs) :
        return self.amount >= rhs
    # end def __ge__

    @_binary_operator
    def __gt__ (self, rhs) :
        return self.amount > rhs
    # end def __gt__

    @_binary_operator
    def __le__ (self, rhs) :
        return self.amount <= rhs
    # end def __le__

    @_binary_operator
    def __lt__ (self, rhs) :
        return self.amount < rhs
    # end def __lt__

    ### other operators

    def __repr__ (self) :
        return """%s ("%s")""" % (self.C_Type.__name__, self.amount)
    # end def __repr__

# end class _Currency_

class Currency (_Currency_) :
    """Model a currency using Decimal for representation.

       You can subclass this to parameterize

       - `name`         : default "Eur"
       - `sloppy_name`  : default "�"
       - `decimal_sign` : default "."
       - `sep_1000`     : default ","

       - `C`: context used to create Decimal instances
       - `Q`: a Decimal used for `quantize` (default Decimal ("0.01"))

       >>> Currency (1), Currency (1) * 2, Currency (4) / 3
       (Currency ("1.00"), Currency ("2.00"), Currency ("1.33"))
       >>> c = Currency ("12345.67")
       >>> c, c.as_string (), c.as_string (round = True)
       (Currency ("12345.67"), '12345.67', '12346')
       >>> c.as_string_s (), c.as_string_s (round = True)
       ('12,345.67', '12,346')
       >>> vat = Currency ("1.20")
       >>> c * vat, c / vat
       (Currency ("14814.80"), Currency ("10288.06"))
       >>> c - c / vat
       Currency ("2057.61")
       >>> divmod (c, 5)
       (Currency ("2469.00"), Currency ("0.67"))
       >>> c *= vat
       >>> c
       Currency ("14814.80")
       >>> c /= vat
       >>> c
       Currency ("12345.67")

       >>> c = Currency ("12345.67")
       >>> d = Currency ("12345.67")
       >>> c == d, c != d, c > 12345, d < 12345
       (True, False, True, False)
    """

    _symbol         = "�"

    C     = decimal.Context (prec = 12, rounding = decimal.ROUND_05UP)
    D     = decimal.Decimal
    Q     = decimal.Decimal ("0.01")
    Q_inv = Q ** -1
    U     = decimal.Decimal ("1.")

    def __init__ (self, amount = 0) :
        self.amount = self.normalized_amount (self.D (amount, self.C))
    # end def __init__

    def as_string (self, round = False) :
        if round :
            return "%s" % (int (self.quantize (self.U)), )
        else :
            a, c = self.split ()
            return "%d%s%02d" % (a, self.decimal_sign, c)
    # end def as_string

    def normalized_amount (self, amount) :
        return amount.quantize (self.Q)
    # end def normalized_amount

    def quantize (self, * args, ** kw) :
        return self.__class__ (self.amount.quantize (* args, ** kw))
    # end def quantize

    def rounded_as_target (self) :
        return self.quantize (self.U)
    # end def rounded_as_target

    def split (self) :
        amount = self.amount
        a      = int (amount)
        return a, int ((amount - a) * self.Q_inv)
    # end def split

    def __str__ (self) :
        a, c = self.split ()
        return "%d%s%02d %s" % (a, self.decimal_sign, c, self.symbol)
    # end def __str__

# end class Currency

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Currency
