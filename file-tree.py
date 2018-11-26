#!/usr/bin/env python

import ansigraph
import os
import yaml
import re

def parse_configuration():
  directory = os.environ.get("INVENTORY_DIRECTORY", None)

  errors = []
  if not directory:
      errors.append("Missing INVENTORY_DIRECTORY in environment")
  if errors:
      raise RuntimeError("\n".join(errors))

  return dict(
    directory=directory
  )

def get_files(dir, files=[]):
  for name in os.listdir(dir):
      path = os.path.join(dir, name)
      if os.path.isfile(path):
          files.append(path)
      else:
          get_files(path, files)

  return files

def read_file(file):
  with open(file, 'r') as stream:
      try:
          return  yaml.load(stream)
      except yaml.YAMLError as exc:
          print(exc)

def parse_files(inventory, files):
  # parse each file and add to inventory
  for file in files:
    content = read_file(file)
    groups = file.split('/')
    # parse groups from file names
    for index, group in enumerate(groups[:-1]):
      inventory.add_child_group(group, re.sub('(^.*).(yml|yaml)$', '\\1', groups[index+1]))

    # parse hosts from inside files
    for group in content.keys():
      inventory.add_host(content[group], re.sub('(^.*).(yml|yaml)$', '\\1', groups[-1]))
      inventory.add_host(content[group], group)

def main():
  config = parse_configuration()
  inventory = ansigraph.ansigraph()
  parse_files(inventory, get_files(config['directory']))
  print inventory.dump_json(inventory.get_hosts())

if __name__ == '__main__':
  main()
