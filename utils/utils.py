# -*- coding: utf-8 -*-
#
# - utils -
#
# Collection of functions for the Prodex Python API
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

from . import constants


def normalize_url(url):
    """Normalize the url by removing the final "/" if it exists

    :param url: The given url
    :type url: str
    :return: The normalized url
    :rtype: str
    """
    if url.endswith("/"):
        return url.rpartition("/")[0]


def build_url_base(url):
    """Normalize and build the final url

    :param url: The given url
    :type url: str
    :return: The final url
    :rtype: str
    """
    normalize = normalize_url(url=url)
    final_url = "{url}/api".format(url=normalize)
    return final_url


def create_filters_payload(filters=None):
    """Create the paylod for the request with the given filters

    :param filters: The list of filters, defaults to None
    :type filters: list, optional
    :return: The formated filters
    :rtype: dict
    """
    payload = {}
    if not filters:
        return payload
    for _filter in filters:
        field = _filter[0]
        operators = _filter[1]
        value = _filter[2]
        if isinstance(value, (list, tuple)):
            value = ",".join(str(v) for v in value)
        if isinstance(value, dict):
            if not value.get("id", None):
                raise ValueError("Value object need to have an id.")
            value = value["id"]
        if isinstance(operators, (list, tuple)):
            chain_operators = []
            for operator in operators:
                _operator = constants.OPERATORS.get(operator, None)
                if not _operator:
                    raise ValueError(
                        "{operator} is not a valid operator.".format(
                            operator=operator
                        )
                    )
                chain_operators.append(_operator)
            field = "{field}{chain}".format(
                field=field, chain="".join(chain_operators)
            )
        else:
            operator = operators
            _operator = constants.OPERATORS.get(operator, None)
            if not _operator:
                raise ValueError(
                    "{operator} is not a valid operator.".format(
                        operator=operator
                    )
                )
            if operator not in ["is", "="]:
                field = "{field}{operator}".format(
                    field=field, operator=_operator
                )
        payload[field] = value
    return payload


def create_fields_payload(action=None, fields=None):
    """Creates a payload for all given fields. The action can be "field" or "omit"

    :param action: The action for the request,
    should be "fields" or "omit", defaults to None
    :type action: str, optional
    :param fields: The given fields, defaults to None
    :type fields: list, optional
    :return: The created payload
    :rtype: list
    """
    payload = {}
    if not fields:
        return payload
    payload[action] = ",".join(fields)
    return payload


def create_ordering_payload(order=None):
    """Creates a payload for the given order

    :param order: The order, defaults to None
    :type order: dict, optional
    :raises ValueError: If the order is not a dictionnary
    :return: The created payload
    :rtype: dict
    """
    payload = {}
    if not order:
        return payload
    if not isinstance(order, dict):
        return payload
    direction = order.get("direction", "ASC")
    field = order.get("field", None)
    if direction not in ["ASC", "DESC"]:
        raise ValueError("Direction must be ASC or DESC")
    if direction == "DESC":
        field = "-{field}".format(field=field)
    payload["ordering"] = field
    return payload
