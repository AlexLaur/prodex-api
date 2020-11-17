# -*- coding: utf-8 -*-
#
# - constants -
#
# All constants variables usefull for the API.
#
# Copyright (c) 2020 Prodex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

OPERATORS = {
    "=": "=",
    "is": "=",
    "in": "__in",
    ">": "__gt",
    ">=": "__gte",
    "<": "__lt",
    "<=": "__lte",
    "isnull": "__isnull",
    "range": "__range",
    "exact": "__exact",  # Case sensitive
    "iexact": "__iexact",  # Case insensitive
    "contains": "__contains",  # Case sensitive
    "icontains": "__icontains",  # Case insensitive
    "startswith": "__startswith",  # Case sensitive
    "istartswith": "__istartswith",  # Case insensitive
    "endswith": "__endswith",  # Case sensitive
    "iendswith": "__iendswith",  # Case insensitive
    "regex": "__regex",  # Case sensitive
    "iregex": "__iregex",  # Case insensitive
    "year": "__year",
    "iso_year": "__iso_year",
    "month": "__month",
    "day": "__day",
    "week": "__week",
    "week_day": "__week_day",
    "quarter": "__quarter",
    "time": "__time",
    "hour": "__hour",
    "minute": "__minute",
    "second": "__second",
}
