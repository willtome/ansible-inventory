# Ansible-Inventory

This repository is a collection of Ansible inventory scripts for different scenarios. These scripts are designed to be used in compatible with Ansible Tower.

## File Tree
The file tree inventory script is intended to use a filesystem hierarchy to describe Ansible groups, children, and nodes. Each child folder will be a a child group. YAML files in found in the folders will be parsed. They are expected to contain lists of nodes. Each "key" will be a group and the nodes listed under each key will be a members of the that group and of the folder. To define variables for the groups or hosts use the `group_vars` or `host_vars` directory adjacent to the inventory script itself. For an example, see the `tests` directory. 

### Using in Ansible Tower
These scripts may rely on networkx for mapping and traversing the inventory. This library is not installed on Tower by default. To install, follow the below instructions.
1. Connect to the command line of your Ansible Tower server and elevate to root.
1. Activate the python virtual environment by running `. /var/lib/awx/venv/ansible/bin/activate`
1. Install the networkx package by running `pip install networkx`
