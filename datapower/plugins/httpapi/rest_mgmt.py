
from __future__ import absolute_import, division, print_function
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils._text import to_text
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
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response, response_data = self.connection.send(
            path, data, headers=headers, method=method
        )
        return handle_response(response, response_data)


def handle_response(response, response_data):
    try:
        response_data = json.loads(response_data.read())
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
