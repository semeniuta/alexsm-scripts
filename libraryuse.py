#
# Piped with output from the following command:
# egrep -r "(import flexvi|from flexvi)" --include \*.ipynb --include \*.py .
#

import fileinput
import re
import json

def add_to_res(res_dict, key, value):

    if key not in res_dict:
        res_dict[key] = []
    res_dict[key].append(value)

regex_import_x = r'^import'
regex_from_x_import = r'^from.*import'

res = dict()

for line in fileinput.input():

    user, import_string = line.split(':')

    if re.search(regex_import_x, import_string):
        module = import_string.split(' ')[1]        
        add_to_res(res, module, user)

    if re.search(regex_from_x_import, import_string):

        module_base, remainder = import_string.split(' import ')
        module_base = module_base.split(' ')[1].strip()

        several_rel_modules = re.search(r',', remainder)
        if several_rel_modules:
            rel_modules = remainder.split(',')
            for rm in rel_modules:
                module = '{}.{}'.format(module_base, rm.strip())
                add_to_res(res, module, user)
        else:
            module = '{}.{}'.format(module_base, remainder.strip())
            add_to_res(res, module, user)


for module, users in res.items():
    print(module, users)
