# Ansible-Inventory

This repository is a collection of Ansible inventory scripts for different scenarios. These scripts are designed to be used in compatible with Ansible Tower.

- [Plugins](#Plugins)
- [Scripts](#Scripts)
- [Roles](#Roles)

# Plugins

## SQLite
The SQLite inventory plugin is an example of a simple inventory plugin to read from a SQLite database. In the `tests/` directory you will find an example of it's execution. The script expects the schema of the SQLlite DB to be in the form below:

| id | name | ip | groups |
|:-----------------------:|:------------------:|:------------:|:--------------------------:|
| auto-incremented number | inventory_hostname | ansible_host | comma separated group list |

An example of creating and loading data can can be found in `tests/sqlite_setup.sh`. There are 2 configurable options for this plugin, `db_path` and `db_table`
- `db_path`: the path to the SQLite DB file
- `db_table`: the table within the DB to lookup hosts

Test command ran from inside the tests dir `ansible-playbook -i sqlite.yml print.yml`

To preview the inventory from the root of the directory `ansible-inventory -i sqlite.yml --list`

## Tower
The Tower inventory plugin allows you dynamically query an existing Tower inventory. This version adds the ability to specify a `parent_group` which will restrict the plugin to only hosts that are children of that group. This search is done recursively. Groups structure of each host is preserved. An example can be found in `tests/tower.yml`.

This plugin required `networkx` be installed. You may need to setup an Ansible [environment](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#common-environment-setup) to test.

Test command `ansible-playbook -i tower.yml print.yml`

## Stacked Plugins
Inventory plugins may be "stacked" as described [here](https://docs.ansible.com/ansible/latest/plugins/inventory.html#using-inventory-plugins). These will execute in order they are in the directory specified. It is a good idea to explitly order using number prefixes such as `00-`, `01-`, etc. See example in `tests/stacked_plugins`.

Test command `ansible-playbook -i stacked_plugins/ print.yml`

# Scripts
## File Tree
The file tree inventory script is intended to use a filesystem hierarchy to describe Ansible groups, children, and nodes. Each child folder will be a a child group. YAML files in found in the folders will be parsed. They are expected to contain lists of nodes. Each "key" will be a group and the nodes listed under each key will be a members of the that group and of the folder. To define variables for the groups or hosts use the `group_vars` or `host_vars` directory adjacent to the inventory script itself. For an example, see the `tests` directory.

### Using in Ansible Tower
These scripts may rely on networkx for mapping and traversing the inventory. This library is not installed on Tower by default. To install, follow the below instructions.
1. Connect to the command line of your Ansible Tower server and elevate to root.
2. Activate the python virtual environment by running `. /var/lib/awx/venv/ansible/bin/activate`
3. Install the networkx package by running `pip install networkx`

# Roles
## Inventory Report
The inventory-report role will calculate the total number of nodes owned by each organization in Tower and produce an html report. Additionally, it will provide a count of total unique nodes based on `inventory_hostname` and a variable. The default variable is `ansible_host`. The quota for unique is defaulted to your total license count. This may or may not match your reported license usage in Tower as Tower only looks at unique hosts based on `inventory_hostname`. https://docs.ansible.com/ansible-tower/latest/html/administration/license-support.html#node-counting-in-licenses

 You can also provide org quotas and the report will highlight if a specific org has exceeded it's given quota. See `report-playbook.yml` for an example of how to use this role and set quotas. The report will look like the table below but in a file called `report.html` in the `playbook-dir`.

| Organization | Nodes | Quota |
|:------------:|:-----:|:-----:|
| Cloud        | 10    | 20    |
| Default      |<span style="background:yellow"> 33 </span>| 20 |
| Network Eng  | 5     | 10    |
| Network Ops  | 15    | 20    |
| Windows      | 0     | N/A   |
| Unix         | 10    | N/A   |
| **Unique** | **73**    | **100**   |

### Using in Ansible Tower
1. Import this repository into your Ansible Tower Server as a project
2. Create a credentail of type `Ansible Tower`
3. Create a job template from the project you imported to run `report-playbook.yml`
    * Attach your credential to the job template
    * You may over ride the quotas by defining the variable `org_node_quotas` as an extra variable
4. Run you new job template!