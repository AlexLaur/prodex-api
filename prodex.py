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

import os

from utils import constants, utils
from utils.decorators import model_check
from libs.models import Model


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
        self.authenticated_user = None
        self.headers = None

        self.url = utils.build_url_base(url=url)

        self.caller = Model(url=self.url)

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
        self.token, self.authenticated_user = self.caller.connection(
            login=login, password=password
        )
        if not self.token:
            raise ValueError("Token doesn't exists !")

    def set_timeout(self, timeout):
        """Sets the timeout for all request. By default the timeout is set to
        None.

        :param timeout: The timeout in milliseconds
        :type timeout: int
        """
        self.caller.timeout = timeout

    def get_session_token(self):
        """Gets the session token associated with the current session.

            If a session token has already been established, this is returned.

            >>> prodex.get_session_token()
            >>> 76f95ec612c45b1bbc536d6f9ccb9f6779e74e59

        :returns: String containing a session token.
        :rtype: str
        """
        return self.token

    def get_authenticated_user(self):
        """Gets the current athenticated user.

            >>> prodex.get_authenticated_user()
            >>> {"username": "root", ..., "id": 1}

        :returns: Current user as a dictionnary.
        :rtype: dict
        """
        return self.authenticated_user

    @model_check
    def find(self, model, filters=None, fields=None, omit=None, order=None):
        payload = {}
        payload.update(utils.create_filters_payload(filters=filters))
        payload.update(
            utils.create_fields_payload(action="fields", fields=fields)
        )
        payload.update(utils.create_fields_payload(action="omit", fields=omit))
        payload.update(utils.create_ordering_payload(order=order))

        response = self.caller.retrieve(
            endpoint=constants.TRANSLATION.get(model), payload=payload
        )
        return response

    @model_check
    def create(self, model, data):
        """Create a new object of the specified ``model``.

            >>> data = {
            ...     "name": "ProdEx Project",
            ...     "users_assign": [
            ...         {'id': 4, 'model': 'User', 'username': 'callewell2'},
            ...         {'id': 90, 'model': 'User', 'username': 'jocarmody2h'},
            ...         {'id': 569, 'model': 'User', 'username': 'bhucfv'},
            ...     ],
            ...     "thumbnail": "path/to/the/thumbnail.png",
            ... }
            >>> prodex.create(model="Project", data=data)

        :param model: The model type
        :type model: str
        :param data: Dictionary of fields and corresponding values to set
        on the new object. If ``thumbnail`` field is provided, the file path
        will be uploaded to the server in the same time.
        :type data: dict
        :return: The created object
        :rtype: dict
        """
        data = utils.data_conformation(data=data)
        response = self.caller.create(
            endpoint=constants.TRANSLATION.get(model), data=data
        )
        return response

    @model_check
    def update(self, model, model_id, data, m2m_modes=None):
        data = utils.data_conformation(data=data)
        endpoint = constants.TRANSLATION.get(model)
        thumbnail = data.pop("thumbnail", None)
        files = None
        if thumbnail:
            files = utils.prepare_thumbnail_file(path=thumbnail)
        if not m2m_modes:
            response = self.caller.update(
                endpoint=endpoint,
                model_id=model_id,
                data=data,
                files=files,
            )
        else:
            # need to retrieve all informations because we need to make a put
            # request for updating m2m fields.
            if not isinstance(m2m_modes, dict):
                raise ValueError("m2m_modes attribut must be a dict.")

            fields = list(m2m_modes.keys())
            payload = {"id": model_id}
            payload.update(
                utils.create_fields_payload(action="fields", fields=fields)
            )
            initial_data = self.caller.retrieve(
                endpoint=endpoint, payload=payload
            )
            if not initial_data:
                raise ValueError(
                    "No object found for model {model} and id {model_id}".format(
                        model=model, model_id=model_id
                    )
                )
            initial_data = utils.data_conformation(data=initial_data[0])
            modified_data = utils.many_to_many_data_constructor(
                initial_data=initial_data,
                data=data,
                m2m_modes=m2m_modes,
            )
            # update data dict in order to get the full data to update
            m2m_fields = list(m2m_modes.keys())
            for m2m_field in m2m_fields:
                data.pop(m2m_field, None)
            modified_data.update(data)

            response = self.caller.update(
                endpoint=endpoint,
                model_id=model_id,
                data=modified_data,
                files=files,
            )
        return response

    @model_check
    def delete(self, model, model_id):
        """Delete the specified model.

        Models in ProdEx are not “deleted” destructively.
        They are instead, “trashed”. This means their ``trashed_at`` field
        is set with the datetime of the deletion.

        The model can be brought back to life
        using :meth:`~prodex_api.ProdEx.restore`.

            >>> prodex.delete(model="Project", model_id=1995)

        .. note::
            To put a model in the trash you can olso use
            :meth:`~prodex_api.ProdEx.update` by setting the ``trashed_at``
            field with the desired datetime.

        .. note::
            An model can be deleted destructively by delete it a second time.

        :param model: The model type
        :type model: str
        :param model_id: The id of the model to delete
        :type model_id: int
        :return: The deleted model
        :rtype: dict
        """
        response = self.caller.delete(
            endpoint=constants.TRANSLATION.get(model),
            model_id=model_id,
        )
        return response

    @model_check
    def restore(self, model, model_id):
        """Restore a model that has previously been deleted.

            >>> prodex.restore(model="Project", model_id=3)

        .. note::
            A deleted object is an object with a value on
            its ``trashed_at`` field. You can olso restore an object with
            the :meth:`~prodex_api.Prodex.update` by setting the ``trashed_at``
            field to ``None``.

        :param model: The model type
        :type model: str
        :param model_id: The id of the model to restore
        :type model_id: str
        :return: The restored project
        :rtype: dict
        """
        response = self.caller.restore(
            endpoint=constants.TRANSLATION.get(model),
            model_id=model_id,
        )
        return response

    @model_check
    def get_schema_fields(self, model):
        response = self.caller.retrieve_schema_fields(
            endpoint=constants.TRANSLATION.get(model)
        )
        return response

    @model_check
    def get_fields(self, model):
        """Return all available fields on the specified model.

            >>> prodex.get_fields(model="Project")
            >>> ['id', 'name', 'customer', 'status', 'description', 'reference',
            'location', 'starts_at', 'ends_at', 'thumbnail', 'estimated_time',
            'metadata', 'created_at', 'updated_at', 'created_by', 'updated_by',
            'trashed_at', 'archived_at', 'production_manager', 'users_assign']

        :param model: The model to get fields.
        :type model: str
        :return: list of all fields
        :rtype: list
        """
        response = self.caller.retrieve_fields(
            endpoint=constants.TRANSLATION.get(model)
        )
        return response

    @model_check
    def upload_thumbnail(self, model, model_id, path):
        """
        Upload a file from a local path and assign it as the thumbnail
        for the specified model.

        .. note::
            Images will automatically be re-sized on the server to generate a
            size-appropriate image file. The final format will be a jpg.

        .. note::
            The updated model is returned when the process is done.
            The thumbnail filename will be `processing.jpg`, because the
            cropping process is done in a separate task. When the process
            is done in the server, the right image path is returned in the
            thumbnail field.

        Supported image file types include ``.jpg`` and ``.png`` (preferred)
        But will also accept ``.gif``, ``.tif``, ``.tiff``, ``.bmp``,
        ``.exr``, ``.dpx``, and ``.tga``.

        :param model: Model to set the thumbnail for
        :type model: str
        :param model_id: Id of the model to set the thumbnail for.
        :type model_id: int
        :param path: Full path to the thumbnail file on disk.
        :type path: str
        :return: The model updated
        :rtype: dict
        """
        files = utils.prepare_thumbnail_file(path=path)
        response = self.caller.update(
            endpoint=constants.TRANSLATION.get(model),
            model_id=model_id,
            files=files,
        )
        return response

    def get_projects_user(self, user_id):
        """Return all projects assigned to an user.

        .. note::
            This method is a shortcut of the :meth:`~prodex_api.Prodex.find`.
            Indeed the same result can be done by getting all ``Project``
            where the ``user_id`` is on ``users_assign`` or ``project_manager``.

        :param user_id: Id of the user.
        :type user_id: int
        :return: list of projects
        :rtype: list
        """
        endpoint = "users/{user_id}/projects".format(user_id=user_id)
        response = self.caller.retrieve(endpoint=endpoint)
        return response

    def get_task_status(self, task_id):
        endpoint = "task-status/{task_id}".format(task_id=task_id)
        response = self.caller.retrieve(endpoint=endpoint)
        return response


if __name__ == "__main__":
    from pprint import pprint

    prodex = ProdEx(
        url="http://127.0.0.1:8000/", login="root", password="PRODEX"
    )
    # users = prodex.find(
    #     "User",
    #     fields=["id", "first_name", "last_name"],
    #     order={"field": "first_name", "direction": "ASC"},
    # )
    #
    # pprint(users)
    project = prodex.find("Project", filters=[["id", "is", 5]])
    pprint(project)
    data = {"users_assign": [10], "name": "Rongle"}
    result = prodex.update(
        "Project", model_id=5, data=data, m2m_modes={"users_assign": "add"}
    )
    pprint(result)
    # path = "/home/alaurette/Téléchargements/image.jpg"
    # pprint(prodex.upload_thumbnail("Project", model_id=5, path=path))
