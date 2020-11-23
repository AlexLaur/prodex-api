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


class NotAuthenticated(ApiError):
    """Raised when the authentication process failed"""

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
        """Initialize the connection with the application thanks to the given
        credentials. If the credentials are corrects, the session token
        and the authenticated user is returned.

        :param login: The login as credential
        :type login: str
        :param password: The password as credential
        :type password: str
        :raises NotAuthenticated: If the reponse doesn't contain the session
        token
        :return: The token and the authenticated user
        :rtype: tuple
        """
        data = {"username": login, "password": password}
        response = requests.post(
            "{url}/token-auth/".format(url=self.url), data=data
        )
        check_status_code(response=response, expected=200)
        if not response.json().get("token", None):
            raise NotAuthenticated(response.json())
        token = response.json().get("token")
        user_obj = response.json().get("user")
        self.__generate_headers(token=token)
        return token, user_obj

    def create(self, endpoint, data):
        """Executes a request with the POST method in order to create
        a new entity on the application

        :param endpoint: The endpoint for the creation
        :type endpoint: str
        :param data: The data of the new entity
        :type data: dict
        :return: The created entity if the request is a success
        :rtype: dict
        """
        response = requests.post(
            "{url}/{endpoint}/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
            data=data,
        )
        check_status_code(response=response, expected=201)
        return response.json()

    def retrieve(self, endpoint, payload=None):
        """Executes a request with the GET method in order to retrieve the
        desired ressource.
        The payload is a dictionnary wich contains all filters, all desired
        fields, or all omits fields, and the desired order.

        :param endpoint: The endpoint for retrieve
        :type endpoint: str
        :param payload: The payload, defaults to None
        :type payload: dict, optional
        :return: The result of the request
        :rtype: list
        """
        response = requests.get(
            "{url}/{endpoint}/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
            params=payload,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def update(self, endpoint, model_id, data):
        """Executes a request with the PATCH method in order to update the
        desired ressource.
        If the request is done, the updated entity is returned.

        :param endpoint: The endpoint for the update
        :type endpoint: str
        :param model_id: The id of the model to update
        :type model_id: int
        :param data: The data for the model to update
        :type data: dict
        :return: The updated model
        :rtype: data
        """
        response = requests.patch(
            "{url}/{endpoint}/{model_id}/".format(
                url=self.url, endpoint=endpoint, model_id=model_id
            ),
            headers=self.headers,
            data=data,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def delete(self, endpoint, model_id):
        """Executes a request with the DELETE method in order to delete the
        desired ressource.

        :param endpoint: The endpoint for the deletion
        :type endpoint: str
        :param model_id: The id of the model to delete
        :type model_id: int
        :return: The deleted ressource
        :rtype: dict
        """
        response = requests.delete(
            "{url}/{endpoint}/{model_id}/".format(
                url=self.url, endpoint=endpoint, model_id=model_id
            ),
            headers=self.headers,
        )

        check_status_code(response=response, expected=204)
        return response.json()

    def restore(self, endpoint, model_id):
        """Execute a request with the PATCH method in order to restore a
        deleted ressource.

        :param endpoint: The endpoint for the restore
        :type endpoint: str
        :param model_id: The id of the model to restore
        :type model_id: int
        :return: The restored ressource
        :rtype: dict
        """
        response = requests.patch(
            "{url}/{endpoint}/{model_id}/restore/".format(
                url=self.url, endpoint=endpoint, model_id=model_id
            ),
            headers=self.headers,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def retrieve_fields(self, endpoint):
        """Executes a request with the GET method in order to get all fields
        of a model.

        :param endpoint: The endpoint for the request
        :type endpoint: str
        :return: The list of all fields
        :rtype: list
        """
        response = requests.get(
            "{url}/{endpoint}/fields/".format(url=self.url, endpoint=endpoint),
            headers=self.headers,
        )

        check_status_code(response=response, expected=200)
        return response.json()

    def retrieve_schema_fields(self, endpoint):
        """Executes a request with the OPTIONS method in order to get the
        schema of a model.

        :param endpoint: The endpoint for the request
        :type endpoint: str
        :return: The schema of the model
        :rtype: dict
        """
        response = requests.options(
            "{url}/{endpoint}/".format(url=self.url, endpoint=endpoint),
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
