# -*- coding: utf-8 -*-
#
# - examples -
#
# Some examples how to use the prodex_api.
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

from prodex_api import Prodex

login = "root"
password = "PRODEX"
# Initialize the client
prodex = Prodex(url="http://localhost:8000/", login=login, password=password)

# Get all projects
# projects = prodex.find("Project")

# Get all projects where id <= 100 and get only the name and the id
filters = [["id", "<=", 100]]
fields = ["id", "name"]
projects = prodex.find("Project", filters=filters, fields=fields)

# Get all projects where id <= 100, id >= 50 and get only the name and the id
filters = [["id", "<=", 100], ["id", ">=", 50]]
fields = ["id", "name"]
projects = prodex.find("Project", filters=filters, fields=fields)

# Get all projects where id <= 100, id >= 50, name startswith "S"
# and get only the name and the id
filters = [["id", "<=", 100], ["id", ">=", 50], ["name", "startswith", "S"]]
fields = ["id", "name"]
projects = prodex.find("Project", filters=filters, fields=fields)

# Get all projects where id <= 100, id >= 50, name contains "Str",
# get only the name and the id and ordering by name DESC
filters = [["id", "<=", 100], ["id", ">=", 50], ["name", "contains", "Str"]]
order = {"field": "name", "direction": "DESC"}
fields = ["id", "name"]
projects = prodex.find("Project", filters=filters, fields=fields, order=order)
