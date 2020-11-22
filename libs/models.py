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


class ApiError(Exception):
    """Raised when no other Exception exists for the code"""

    pass


class BadRequest(ApiError):
    """Raised when status code is 400"""

    pass


class Unauthorized(ApiError):
    """Raised when status code is 401"""

    pass


class Forbidden(ApiError):
    """Raised when status code is 403"""

    pass


class NotFound(ApiError):
    """Raised when status code is 404"""

    pass


class RequestTimeout(ApiError):
    """Raised when status code is 408"""

    pass


class InternalServerError(ApiError):
    """Raised when status code is 500"""

    pass


class ServiceUnavailable(ApiError):
    """Raised when status code is 503"""

    pass


class Model(object):
    def __init__(self, url):

        self.headers = None
        self.timeout = None
        self.url = url

        self.__ping_url()

    def __ping_url(self):
        """Test the connection between the client and the prodex API"""
        # try:
        #     request = requests.get(self.url, timeout=self.timeout)
        # except (requests.ConnectionError, requests.Timeout) as exception:
        #     raise requests.ConnectionError
        pass

    def __generate_headers(self, token):
        """Build the header for all request"""
        self.headers = {"Authorization": "Token {token}".format(token=token)}

    def connection(self, login, password):
        data = {"username": login, "password": password}

        response = requests.post(
            "{url}/token-auth/".format(url=self.url), data=data
        )

        check_status_code(response=response, expected=200)

        if not response.json().get("token", None):
            # TODO raise authentication error
            ...

        token = response.json().get("token")
        user_obj = response.json().get("user")

        self.__generate_headers(token=token)

        return token, user_obj

    def create(self, endpoint, data):
        response = requests.post(
            "{url}/{endpoint}/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
            data=data,
        )
        check_status_code(response=response, expected=201)
        return response.json()

    def retrieve(self, endpoint, payload=None):
        response = requests.get(
            "{url}/{endpoint}/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
            params=payload,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def update(self, endpoint, model_id, data):
        pass

    def delete(self, endpoint, model_id):
        response = requests.delete(
            "{url}/{endpoint}/{model_id}/".format(
                url=self.url, endpoint=endpoint, model_id=model_id
            ),
            headers=self.headers,
        )

        check_status_code(response=response, expected=204)
        return response.json()

    def restore(self, endpoint, model_id):
        response = requests.patch(
            "{url}/{endpoint}/{model_id}/restore/".format(
                url=self.url, endpoint=endpoint, model_id=model_id
            ),
            headers=self.headers,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def retrieve_schema(self, endpoint):
        response = requests.get(
            "{url}/{endpoint}/fields/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
        )

        check_status_code(response=response, expected=200)
        return response.json()


def check_status_code(response, expected):
    """Raise arrors if the status code doesn't match with the expected code

    :param response: The current status code
    :type response: int
    :param expected: The expected status code
    :type expected: int
    """
    if isinstance(expected, int):
        expected = [expected]
    status_code = response.status_code
    if status_code not in expected:
        if status_code == 400:
            raise BadRequest(response.json())
        elif status_code == 401:
            raise Unauthorized(response.json())
        elif status_code == 403:
            raise Forbidden(response.json())
        elif status_code == 404:
            raise NotFound(response.json())
        elif status_code == 408:
            raise RequestTimeout(response.json())
        elif status_code == 500:
            raise InternalServerError(response.json())
        elif status_code == 503:
            raise ServiceUnavailable(response.json())
        else:
            raise ApiError(response.json())
