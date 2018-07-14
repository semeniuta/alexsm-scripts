"""
Exploring possibilities for listing all modules in standard library

Ideas from:
https://stackoverflow.com/questions/8370206/how-to-get-a-list-of-built-in-modules-in-python
"""

import os
import sys
import pkgutil
from pprint import pprint


def get_set_of_standard_modules():

    d = dict()
    all_module_names = []

    faulty = []

    for m in pkgutil.iter_modules():

        all_module_names.append(m.name)

        if hasattr(m.module_finder, 'path'):
            path = m.module_finder.path
        elif hasattr(m.module_finder, 'archive'):
            path = m.module_finder.archive
        else:
            raise Exception('Strange module: {}'.format(m))

        if path not in d:
            d[path] = [m.name]
        else:
            d[path].append(m.name)

    distro_base_path = sys.executable.split('bin/python')[0]

    std_paths = (
        os.path.join(distro_base_path, 'lib', 'python3.6', 'lib-dynload'),
        os.path.join(distro_base_path, 'lib', 'python3.6')
    )

    std_modules = []
    for dir_name, modules_list in d.items():

        if dir_name in std_paths:
            std_modules += modules_list

    std_modules += list(sys.builtin_module_names)

    return set(std_modules), d


if __name__ == '__main__':

    std_modules, modules_dict = get_set_of_standard_modules()

    print('All modules:')
    pprint(modules_dict)

    print()
    print('Standard modules:')
    pprint(std_modules)
