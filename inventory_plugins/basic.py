DOCUMENTATION = r'''
    name: Inventory Plugin Basics
    plugin_type: inventory
    author:
      - Alan Rominger (@AlanCoding)
      - Will Tome (@willtome)
    short_description: Used for instructive purposes.
    version_added: "2.10"
    description:
        - Demonstrates basics of a custom inventory plugin.
    options:
        host_base:
            description: The base of host names.
            type: string
            default: host_
            required: False
        count:
            description: The number of hosts and groups to make.
            type: integer
            required: True
        password:
            description: Password to put in hostvars b64 encoded.
            type: string
            secret: true
            default: foo
            env:
                - name: BASIC_PASSWORD
    requirements:
        - python >= 3.4
'''

EXAMPLES = r'''
# create 4 sub-groups and hosts
plugin: basic
count: 4
'''

# Ansible internal request utilities
from ansible.module_utils.six.moves.urllib.parse import urljoin
from ansible.module_utils.urls import Request, ConnectionError, urllib_error

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin

from base64 import b64encode


import json


class InventoryModule(BaseInventoryPlugin):

    NAME = 'basic'

    def verify_file(self, path):  # Plugin interface (1)
        super(InventoryModule, self).verify_file(path)
        return path.endswith(('basic.yml', 'basic.yaml'))

    def parse(self, inventory, loader, path, cache=True):  # Plugin interface (2)
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)
        base_name = self.get_option('host_base')
        count = self.get_option('count')

        root_group_name = self.inventory.add_group('root-group')  # Inventory interface (3)

        for i in range(count):
            group_name = self.inventory.add_group('{}group_{}'.format(base_name, count))  # Inventory interface (3)
            self.inventory.add_child(root_group_name, group_name)  # Inventory interface (5)
            host_name = self.inventory.add_host('{}{}'.format(base_name, count))  # Inventory interface (1)
            self.inventory.add_child(group_name, host_name)  # Inventory interface (4)

        self.inventory.set_variable(
            root_group_name, 'hashed_password',
            str(b64encode(bytes(self.get_option('password'), encoding='utf8')), encoding='utf8')
        )  # inventory interface (2)
