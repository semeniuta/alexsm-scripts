"""
Visualize the file system structure 
of the result of find command. 

Usage example:
find . -name "*.ipynb" ! -name "*-checkpoint.ipynb" | python /path/to/findtree.py
"""

import fileinput
import re
from pprint import pprint


def insert(d, key):
    if key not in d:
        d[key] = {}


def fill(d, first, rest):
    
    insert(d, first)

    parent = d[first]
    for el in rest:
        insert(parent, el)
        parent = parent[el]


def print_tree(d):

    def p(prefix, d):

        for k, v in d.items():
            print('{}{}'.format(prefix, k))
            p(prefix+'\t', v)

    p('', d)


if __name__ == '__main__':

    d = {}

    for line in fileinput.input():
        
        line = line[2:]
        
        elements = line.split('/')
        elements = list(map(lambda x: x.strip(), elements))

        first = elements[0]
        rest = elements[1:]

        fill(d, first, rest)
    
    print_tree(d)            
