#
# Piped with output from the find command, e.g.:
# find . -name '*.ipynb' ! -name '*-checkpoint.ipynb'
#

# TODO

import fileinput
import re

res = {}

for line in fileinput.input():
    
    line = line[2:]
    #print(line)
    #continue
    
    elements = line.split('/')
    
    d = res
    for el in elements[:-2]:
        if el not in d:
            d[el] = {}
        d = d[el]
        
    last_dir = elements[-2]
    fname = elements[-1]
    if last_dir not in d:
        d[last_dir] = []   
    d[last_dir] = fname  
    
    
    
        