from __future__ import absolute_import, division, print_function
try:
    from ansible_collections.community.datapower.plugins.module_utils.datapower.files import (
        LocalFile,
        LocalDirectory
    )
except:
    from files import *
try:
    from ansible_collections.community.datapower.plugins.module_utils.datapower.classes import valid_objects
except:
    from classes import *
    
import posixpath 

__metaclass__ = type

class Config():

    # domain and class_name are the bare minimum required to get a valid
    # response from DataPower
    def __init__(self, domain, config=None, class_name=None, name=None, field=None):
        self.domain = domain
        self.set_class_name(class_name, config)
        self.set_name(name, config)
        self.set_config(config)
        self.field = field

    def set_config(self, config=None):
        if not config:
            self.config = None
            return
        # This will build a valid body that will work for POST and PUT methods.
        if self.class_name in config:
            if self.name in config[self.class_name]:
                self.config = config
            else:
                config[self.class_name]['name'] = self.name
                self.config = config
        else:
            if self.name not in config:
                config['name'] = self.name
            self.config = {
                self.class_name: config
            }
    
    def set_options(self, options):
        self.options = options

    # Try to set class_name allowing for some flexibility
    # it can be set by specifying it as class_name
    # or within the config dictionary
    def set_class_name(self, class_name=None, config=None):
        if class_name and is_valid_class(class_name):
            self.class_name = class_name
        elif config and is_valid_class(list(config.keys())[0]):
            self.class_name = list(config.keys())[0]
        else:
            raise ValueError('Invalid class_name or no class_name provided.')

    # Try to set name, the module allows for some flexibility
    # it can be set by specifying it as name
    # or within the config dictionary
    def set_name(self, name=None, config=None):
        if not name:
            if self.class_name in config:
                self.name = config.get(self.class_name).get('name')
            elif 'name' in self.config:
                self.name = config.get('name')
            else:
                raise AttributeError('name attribute is required.')
        else:
            self.name = name

class DPActionQueue():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class DPGetConfigObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class DPManageConfigObject:
    # domain and class_name are the bare minimum required to get a valid
    # response from DataPower
    # kwargs consisting of the arguments defined in the Ansible Modules
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Try to set class_name, the module allows for some flexibility
        # it can be set by specifying it as class_name
        # or within the config dictionary
        if not hasattr(self, 'class_name') or self.class_name is None:
            self.class_name = list(self.config.keys())[0]
            if not is_valid_class(self.class_name):
                raise ValueError(
                    'Invalid class_name or no class_name provided.')

        # Try to set name, the module allows for some flexibility
        # it can be set by specifying it as name
        # or within the config dictionary
        if not hasattr(self, 'name') or self.name is None:
            if self.class_name in self.config:
                self.name = self.config.get(self.class_name).get('name')
            elif 'name' in self.config:
                self.name = self.config.get('name')
            else:
                raise AttributeError('name attribute is required.')

# This is hardcoded, the response is from DataPower v 10.0.1.0.
# This should greatly improved by having it check at the beginning
# of module execution

def is_valid_class(class_name):
    return class_name in valid_objects

# This is first attempt at creating these objects with inheritence, DPFile and DPDirectory.
# Dependent on success / value in doing this the above objects will follow suite.
# DPFile and DPDirectory are direct representations of all the attributes/parameters
# required to create a file / directory on DataPower's filesystem.

class DPObject():
    def __init__(self, domain: str):
        self.domain = domain

    def __str__(self):
        return "domain: " + self.domain


def get_parent_dir(path):
    return posixpath.split(path)[0]


def clean_dp_path(path):
    return path.rstrip('/').lstrip('/')


def get_dest_file_path(dest):
    if len(dest.split('/')) == 2: #Accounts for creating a file at the root of a top_directory
        dest_file_path = dest.split('/')[-1] 
    elif len(dest.split('/')) > 2:
        dest_file_path = '/'.join(dest.split('/')[1:])
    else: # len < 2
        raise Exception('Must specify full file path in destination, ie local/full/path/to/file.txt')
    return dest_file_path


def get_top_dir(dest):
    top_dir = clean_dp_path(dest).split('/')[0]
    for dir_ in TOP_DIRS:
        if dir_ in top_dir:
            return dir_
    else:
        raise Exception(
            top_dir +' is an invalid top directory, must be one of ', ' '.join(TOP_DIRS)
        )


class DPDirectory():

    def __init__(self, dest):
        dir_path = dest.split('/')[1:-1]
        if dest.split('/')[0] != 'local':
            raise InvalidDPDirectoryException('Subdirectories are only valid in local/')
        else:
            root = dest.split('/')[0]

    @staticmethod
    def get_root_dir(path):
        if 'local' not in path:
            raise AttributeError('can only create local direct')
        else:
            return True


class InvalidDPDirectoryException(Exception):
    pass


if __name__ == '__main__':
    domain = 'default'
    file_path = '/Users/anthonyschneider/DEV/ansible-datapower-playbooks/collections/ansible_collections/community/datapower/tests/unit/module_utils/test_data/copy/test/to/GetStat/getCPU.js'
    lf = LocalFile(file_path)
    obj = DPFile(domain, content=lf.get_base64(), path='local/GetStat/getCPU.js')
    print(obj.__str__())
