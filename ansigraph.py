
import networkx as nx
import json

class ansigraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.inventory = {}

    def add_host(self, host, group):
      if isinstance(host, basestring):
        self.graph.add_node(host, type='host')
        self.graph.add_edge(group,host)
      else:
        self.graph.add_nodes_from(host, type='host')
        self.add_group(group)
        for item in host:
          self.graph.add_edge(group, item)

    def add_group(self, group):
        self.graph.add_node(group, type='group')

    def add_child_group(self, parent, child):
        self.graph.add_node(parent, type='group')
        self.graph.add_node(child, type='group')
        self.graph.add_edge(parent,child)

    def add_parent_group(self, parent, child):
        self.graph.add_edge(parent,child)

    def get_hosts(self, group=None, recurse=True):
        if group:
          if recurse:
            tree = nx.DiGraph(list(nx.dfs_edges(self.graph,group)))
            return [x for x in tree.nodes() if self.graph.node[x]['type'] == 'host' ]
          else:
            return [x for x in list(self.graph.successors(group)) if self.graph.node[x]['type'] == 'host']
        else:
          return [x for x in self.graph.nodes() if self.graph.node[x]['type'] == 'host']

    def build_inventory(self, start):
        parents = self.graph.predecessors(start)
        if parents:
          for parent in parents:

            if parent not in self.inventory.keys():
              self.inventory[parent] = {
                'children': [],
                'hosts': []
              }

            if self.graph.node[start]['type'] == 'host':
              if start not in self.inventory[parent]['hosts']:
                self.inventory[parent]['hosts'].append(start)
            elif self.graph.node[start]['type'] == 'group':
              if start not in self.inventory[parent]['children']:
                self.inventory[parent]['children'].append(start)

            self.build_inventory(parent)


    def dump_json(self, hosts):
      for host in hosts:
        self.build_inventory(host)

      return json.dumps(self.inventory)

