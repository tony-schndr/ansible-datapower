#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The arg spec for the datapower_domain module
"""


class DomainArgs(object):  # pylint: disable=R0903
    """The arg spec for the datapower_domain module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {'config': {'elements': 'dict',
            'options': {'ConfigDir': {'default': 'config:///', 'type': 'str'},
                        'ConfigMode': {'choices': ['local', 'import'],
                                       'default': 'local',
                                       'type': 'str'},
                        'ConfigPermissionsMode': {'choices': ['scope-domain',
                                                              'global-profile',
                                                              'specific-profile'],
                                                  'default': 'scope-domain',
                                                  'type': 'str'},
                        'ConfigPermissionsProfile': {'type': 'str'},
                        'DeploymentPolicy': {'type': 'str'},
                        'DeploymentPolicyParameters': {'type': 'str'},
                        'DomainUser': {'elements': 'str', 'type': 'list'},
                        'FileMap': {'options': {'CopyFrom': {'choices': ['on',
                                                                         'off'],
                                                             'type': 'str'},
                                                'CopyTo': {'choices': ['on',
                                                                       'off'],
                                                           'type': 'str'},
                                                'Delete': {'choices': ['on',
                                                                       'off'],
                                                           'type': 'str'},
                                                'Display': {'choices': ['on',
                                                                        'off'],
                                                            'type': 'str'},
                                                'Exec': {'choices': ['on',
                                                                     'off'],
                                                         'type': 'str'},
                                                'Subdir': {'choices': ['on',
                                                                       'off'],
                                                           'type': 'str'}},
                                    'type': 'dict'},
                        'ImportFormat': {'choices': ['ZIP', 'XML'],
                                         'default': 'ZIP',
                                         'type': 'str'},
                        'ImportURL': {'type': 'str'},
                        'LocalIPRewrite': {'choices': ['on', 'off'],
                                           'default': 'on',
                                           'type': 'str'},
                        'MaxChkpoints': {'default': 3, 'type': 'int'},
                        'MonitoringMap': {'options': {'Audit': {'choices': ['on',
                                                                            'off'],
                                                                'type': 'str'},
                                                      'Log': {'choices': ['on',
                                                                          'off'],
                                                              'type': 'str'}},
                                          'type': 'dict'},
                        'NeighborDomain': {'default': 'default',
                                           'elements': 'str',
                                           'type': 'list'},
                        'UserSummary': {'type': 'str'},
                        'mAdminState': {'choices': ['enabled', 'disabled'],
                                        'default': 'enabled',
                                        'type': 'str'},
                        'name': {'type': 'str'}},
            'type': 'list'},
 'state': {'choices': ['merged', 'replaced', 'overriden', 'deleted'],
           'default': 'merged',
           'type': 'str'}}  # pylint: disable=C0301
