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

import os

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


def data_conformation(data):
    """Conform the data before the API call in order to transform
    all dictionnary, which represent entity like an id.

    :param data: The data to conform
    :type data: dict
    """
    for key, values in data.items():
        if isinstance(values, dict):
            _id = values.get("id", None)
            if not _id:
                raise ValueError("You need to give an id for this.")
            data[key] = _id
        elif isinstance(values, list):
            new_values = []
            for value in values:
                if isinstance(value, dict):
                    _id = value.get("id", None)
                    if not _id:
                        raise ValueError("You need to give an id for this.")
                    new_values.append(_id)
                elif isinstance(value, int):
                    new_values.append(value)
                else:
                    continue
            data[key] = new_values
    return data


def many_to_many_data_constructor(initial_data, data, m2m_modes):
    """Builds the data for the update when the m2m_modes is defined.
    It only update m2m fields with the new data.

    :param initial_data: The initial data before any modification
    :type initial_data: dict
    :param data: The new data to update
    :type data: dict
    :param m2m_modes: The many to many modes
    :type m2m_modes: dict
    :raises TypeError: If the field given in m2m_modes is not
    a many to many field
    :raises ValueError: If the given mode is not "add", "remove" or "set"
    :raises TypeError: If the data for a m2m field is not an array
    :return: The modified data for the update
    :rtype: dict
    """
    fields = list(initial_data.keys())
    _allowed_modes = ["add", "remove", "set"]

    for field, m2m_mode in m2m_modes.items():
        if field not in fields:
            continue
        if not isinstance(initial_data[field], list):
            raise TypeError("{field} is not a m2m field.".format(field=field))
        if m2m_mode not in _allowed_modes:
            raise ValueError(
                "Mode must be in {modes}".format(modes=_allowed_modes)
            )

        _data = data.get(field, None)
        if not _data:
            continue
        if not isinstance(_data, list):
            raise TypeError(
                "data for {field} must be an array.".format(field=field)
            )

        if m2m_mode == "add":
            for value in _data:
                if value in initial_data[field]:
                    continue
                initial_data[field].append(value)

        elif m2m_mode == "remove":
            for value in _data:
                if value in initial_data[field]:
                    initial_data[field].pop(initial_data[field].index(value))

        else:  # set mode by default
            initial_data[field] = _data

    return initial_data


def prepare_thumbnail_file(path):
    """Prepares the given file for an upload as thumbnail

    :param path: The path of the image to upload
    :type path: str
    :raises IOError: If the file doesn't exists
    :return: Dictionnary with the field "thumbnail" as key and the image data
    (binary) as value.
    :rtype: dict
    """
    if not os.path.exists(path):
        raise IOError("The specified file doesn't exists.")
    return {"thumbnail": open(path, "rb")}
