# -*- coding: utf-8 -*-
#
# - decorators -
#
# All decorators usefull for the API.
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


def model_check(func):
    """Checks if the model is referenced as a valid model. If the model is
    valid, the API will be ready to find the correct endpoint for the given
    model.

    :param func: The function to decorate
    :type func: function
    """

    def wrapper(*args, **kwargs):
        model = None
        if kwargs:
            model = kwargs.get("model", None)
        if not model:
            if len(args) > 1:
                model = args[1]  # args[0] is the decorted function
        if not constants.TRANSLATION.get(model, None):
            raise ValueError(
                "'{model}' doesn't exists. Allowed models: {allowed_models}".format(
                    model=model,
                    allowed_models=",\n".join(
                        list(constants.TRANSLATION.keys())
                    ),
                )
            )
        return func(*args, **kwargs)

    return wrapper
