# File Tree

In this example, you will find the file `file-tree.py` which is symlinked to the actual inventory script in the root of the repo. To parse the tree structure under the `sites` directory, set the environment variable `INVENTORY_DIRECTORY` to sites. (ie. `export INVENTORY_DIRECTORY=sites`) The structure of `sites` looks like this:
```
sites
├── apac
│   └── singapore.yml
├── emea
│   └── london.yml
└── us
    ├── central
    │   └── denver.yml
    ├── east
    │   ├── boston.yml
    │   └── raleigh.yml
    └── west
        ├── seattle.yml
        └── sf.yml
```
The top level group will be called `sites` and `apac`,`emea`, and `us` will children and so on. Inside of the .yml files looks something like this:

```london.yml
#sites/emea/london.yml
---
windows:
  - lon-win-01
  - lon-win-02

cisco:
  - lon-cisco-01
  - lon-cisco-02
```
From this, the groups `windows` and `cisco` will be created with the members listed under each. All nodes listed will be added to the `london` group. If any other .yml files contain the groups `windows` or `cisco`, those nodes will be added to the same group but will also have a different parent groups. By using [patterns](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html) you can create very unique selections of nodes from these groups.

**Variables**

In this example, variables are assigned to the groups via the `group_vars` directory. See [this documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#splitting-out-host-and-group-specific-data) for an explaination of how `group_vars` and `host_vars` work. The group_vars structure looks like this:
```
group_vars/
├── apac
│   └── ntp.yml
├── cisco.yml
├── juniper.yml
├── nxos.yml
├── us
│   ├── central
│   │   └── dns.yml
│   ├── east
│   │   └── dns.yml
│   ├── ntp.yml
│   └── west
│       └── dns.yml
└── windows.yml
```
As you notice, some of the group names are directories and some are .yml files. Different variables are defined in different places to show some options.
