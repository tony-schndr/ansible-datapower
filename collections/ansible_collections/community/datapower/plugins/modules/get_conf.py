#!/usr/bin/env python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: community.datapower.get

short_description: Use for geting objects on IBM DataPower


version_added: "1.0.0"

description: Use for getting object configuration

options:
    domain:
        description: Target domain
        required: True
        type: str
    object_class:
        description: DataPower objects object_class.  Determine object_class by...
        required: true
        type: str
    name:
        description: Name of object as seen in DataPwer
    options:
        description: Options for retrieving objects.
        required: False
        type: dict
        recursive:
            description: Get target objects referenced objects.
            required: False
            type: bool
        depth:
            description: Set the depth of the recursion.
            required: False
            type: int
            default: 7
        state:
            description: If true return state information on all returned objects.
            required: False
            type: bool
            default: False


author:
    - Your Name (anthonyschneider)
'''

EXAMPLES = r'''
# Get a datapower object.  Determine object_class by ...
- name: Get the cert Test2
  community.datapower.get_conf:
    domain: "{{ domain }}"
    class_name: CryptoCertificate
    name: Test2
- name: Get the valcred and referenced objects recursively, return state of all objects as well.
  community.datapower.get_conf:
    domain: "{{ domain }}"
    class_name: CryptoValCred
    name: valcred
    recursive: True
    state: True
    depth: 3
- name: Get all valcreds
  community.datapower.get_conf:
    domain: "{{ domain }}"
    class_name: CryptoValCred
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
request:
    description: The request that was sent to DataPower
    type: dict
    returned: always
    sample: {
        "body": null,
        "method": "GET",
        "path": "/mgmt/config/default/CryptoValCred?"
    }

response:
    description: A Dictionary representing the response returned from DataPowers Rest MGMT Interface
    type: dict
    returned: on success
    sample:  {
        "CryptoCertificate": {
            "Filename": "cert:///webgui-sscert.pem",
            "IgnoreExpiration": "off",
            "PasswordAlias": "off",
            "mAdminState": "disabled",
            "name": "Test2"
        },
        "_links": {
            "doc": {
                "href": "/mgmt/docs/config/CryptoCertificate"
            },
            "self": {
                "href": "/mgmt/config/default/CryptoCertificate/Test2"
            }
        }
    }
URLError | HTTPError | ConnectionError:
    description: The error message(s) returned by DataPower
    type: dict
    returned: on failure
    sample: {
        "URLError": "message",
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.datapower.plugins.module_utils.datapower import DPGet, check_for_error

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        domain=dict(type='str', required=True),
        class_name=dict(type='str', required=True),
        name=dict(type='str', required=False),
        obj_field=dict(type='str', required=False),
        recursive=dict(type='bool', required=False),
        depth=dict(type='int', required=False),
        state=dict(type='bool', required=False)
        
    )
    mutually_exclusive = [
        ['obj_field', 'recursive'],
    ]
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive
    )
    
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    #if module.check_mode:
    #    module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    dp_get = DPGet(module)
    result = dp_get.send_request()

    if check_for_error(result):
        module.fail_json(msg="Failed to retrieve configuration", **result)

    result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()