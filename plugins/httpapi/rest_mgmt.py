
from __future__ import absolute_import, division, print_function
from ansible.plugins.httpapi import HttpApiBase
from ansible_collections.community.datapower.plugins.module_utils.datapower.mgmt import (
    clean_dp_dict
)
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils._text import to_text
from xml.sax.saxutils import unescape
import json

__metaclass__ = type

DOCUMENTATION = """
author: Anthony Schneider
httpapi: datapower
short_description: HttpApi Plugin for IBM DataPower
description:
- This HttpApi plugin provides methods to connect to IBM DataPower REST management interface.
version_added: 1.0.0
"""


class HttpApi(HttpApiBase):
    def send_request(self, path, method, data):
        if data:
            data = json.dumps(data)
            clean_dp_dict(data)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response, response_data = self.connection.send(
            path, data, headers=headers, method=method
        )
        return handle_response(response, response_data)

    def get_resource_or_none(self, path):
        try:
            res = self.send_request(path, 'GET', None)
        except ConnectionError as ce:
            err = to_text(ce)
            if 'Resource not found' in err:
                return None
            else:
                raise ce
        return res


def handle_response(response, response_data):

    try:
        # DataPower will sometimes return xml encoded strings, unescape
        # For example &amp is found in strings in AccessProfile and
        # ConfigDeploymentPolicy objects.
        response_data = json.loads(unescape(response_data.read().decode()))

    except ValueError:
        response_data = response_data.read()

    if isinstance(response, HTTPError):
        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join(
                    (error["error-message"] for error in errors)
                )
            else:
                error_text = response_data

            raise ConnectionError(error_text, code=response.code)
        raise ConnectionError(to_text(response), code=response.code)

    return response_data
