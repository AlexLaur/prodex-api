# -*- coding: utf-8 -*-
#
# - model -
#
# Model is a module for all request to the API. Indeed the Python Prodex API is
# build like on a MVC architecture.
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

import requests


def connection(url, login, password):
    data = {"username": login, "password": password}
    try:
        response = requests.post(
            "{url}/token-auth/".format(url=url), data=data
        )
    except requests.exceptions.ConnectionError as error:
        # TODO raise connection error
        return None, None
    if response.status_code != 200:
        # TODO raise bad request
        ...

    if not response.json().get("token", None):
        # TODO raise authentication error
        ...

    token = response.json().get("token")
    user_obj = response.json().get("user")

    return token, user_obj
