# -*- coding: utf-8 -*-
#
# - prodex -
#
# The core of the API for prodex.
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


from utils import constants, utils, decorators
from libs import model


class ProdEx(object):
    def __init__(self, url, login, password):
        """Initializes a new instance of the ProdExp client.

        :param url: The URL for the the api of prodexp
        :type url: str
        :param login: The login to initialize the connection, defaults to None
        :type login: str, optional
        :param password: The password to initialize the connection, defaults to None
        :type password: str, optional
        """
        self.token = None
        self.header = None

        self.url = utils.build_url_base(url=url)

        self.__connect(login, password)

    def __connect(self, login, password):
        """Try to connect to prodex with the given credentials.
        If the connection is done, the token's user
        and the user object is returned.

        :param login: The given login
        :type login: str
        :param password: The given password
        :type password: str
        :raises ValueError: Raise ValueError is token doesn't exists
        """
        self.token, self.user = model.connection(
            url=self.url, login=login, password=password
        )
        if not self.token:
            raise ValueError("Token doesn't exists !")

    def __build_header(self):
        """Build the header for all request."""
        self.header = {
            "Authorization": "Token {token}".format(token=self.token)
        }

    @decorators.model_check
    def find(self, model, filters=None, fields=None):
        payload = utils.create_payload(filters=filters)
        print(payload)

    @decorators.model_check
    def create(self, model, data):
        ...

    @decorators.model_check
    def update(self, model, model_id, data):
        ...

    @decorators.model_check
    def delete(self, model, model_id):
        ...

    @decorators.model_check
    def restore(self, model, model_id):
        ...

    @decorators.model_check
    def get_fields(self, model):
        ...


if __name__ == "__main__":
    prodex = ProdEx(
        url="http://127.0.0.1:8000/", login="root", password="PRODEX"
    )
    prodex.find("User", filters=[["id", "is", 1]])
