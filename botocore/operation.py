# Copyright (c) 2012 Mitch Garnaat http://garnaat.org/
# Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from .parameters import get_parameter
from . import BotoCoreObject


class Operation(BotoCoreObject):

    def __init__(self, endpoint, op_data):
        self.input = {}
        self.output = {}
        BotoCoreObject.__init__(self, **op_data)
        self.endpoint = endpoint
        self.type = 'operation'
        self._get_parameters()

    def __repr__(self):
        return 'Operation:%s' % self.name

    def __call__(self, **kwargs):
        params = self.build_parameters(**kwargs)
        params['Action'] = self.name
        params['Version'] = self.endpoint.service.api_version
        return self.endpoint.make_request(self, params)

    def _get_parameters(self):
        """
        Build the list of Parameter objects for this operation.
        """
        self.params = []
        if self.input and 'members' in self.input:
            for name, data in self.input['members'].items():
                param = get_parameter(name, data)
                self.params.append(param)

    def build_parameters(self, **kwargs):
        """
        Returns a dictionary containing the kwargs for the
        given operation formatted as required to pass to the service
        in a request.
        """
        built_params = {}
        missing = []
        for param in self.params:
            if param.required:
                missing.append(param)
            if param.py_name in kwargs:
                if missing:
                    missing.pop()
                param.build_parameter(kwargs[param.py_name],
                                      built_params)
        if missing:
            msg = 'The following required parameters are missing:'
            msg += ','.join([p.py_name for p in missing])
            raise ValueError(msg)
        return built_params