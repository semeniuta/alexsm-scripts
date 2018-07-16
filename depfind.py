"""
Find dependencies (imported Python modules) recursively in a directory

Usage example:
python depfind.py EPypes/epypes/
"""

import os
import re
import argparse
import pprint
from collections import deque

from stdmodules import get_set_of_standard_modules

IGNORE_DIRS = (r'__pycache__', r'^\..*')


def is_python_file(fname):

    ext = os.path.splitext(fname)[1]
    return ext in ('.py', '.ipynb')


def dir_is_python_package(files_in_dir):
    return '__init__.py' in files_in_dir


def line_has_import(line):
    return 'import ' in line


def get_imported_module_name(line):

    template_1 = 'from [\w\.]+ import'
    template_2 = 'import [\w\.]+'

    match = re.search(template_1, line)
    if match:
        return match.group().split(' ')[1]

    match = re.search(template_2, line)
    if match:
        return match.group().split(' ')[-1]

    return None


def dir_to_ignore(dir_basename):

    for template in IGNORE_DIRS:
        if re.match(template, dir_basename):
            return True

    return False


def classify_imports(all_imports, all_scripts):

    std_modules, _ = get_set_of_standard_modules()

    imports = deque(all_imports.keys())

    imports_std = set()
    imports_internal = set()
    imports_external = set()

    #for imp in imports:
    while len(imports) > 0:

        imp = imports.pop()

        if imp in std_modules:
            imports_std.add(imp)
            continue

        if import_is_internal(imp, all_scripts):
            imports_internal.add(imp)
            continue

        imports_external.add(imp)


    return imports_external, imports_internal, imports_std


def import_is_internal(imp, scripts_dict):

    components = imp.split('.')
    main_comp = components[-1]

    if not main_comp in scripts_dict:
        return False

    for detailed_tuple in scripts_dict[main_comp]:

        res = True
        for i, comp in enumerate(reversed(components[:-1])):
            if comp != detailed_tuple[i]:
                res = False
                continue

    return res


def search(search_path, verbose):

    imports = {}
    scripts = {}
    packages = set()

    for root, dirs, files in os.walk(search_path):

        dir_basename = os.path.basename(root)

        if dir_to_ignore(dir_basename):
            if verbose:
                print('Ignoring', dir_basename)
            continue

        if dir_is_python_package(files):
            packages.add(root)

        if verbose:
            print('Directory:', root)

        python_files = filter(is_python_file, files)

        for fname in python_files:

            full_fname = os.path.join(root, fname)

            module_name = fname[:-3] # without .py

            rev = tuple(reversed(full_fname.split('/')))[1:-1]
            if module_name not in scripts:
                scripts[module_name] = [rev]
            else:
                scripts[module_name].append(rev)

            with open(os.path.join(root, fname)) as f:

                lines = (line for line in f)
                lines_with_import = filter(line_has_import, lines)

                for line in lines_with_import:

                    module_name = get_imported_module_name(line)
                    line_content = line.strip()

                    if verbose:
                        print('{}: {} => {}'.format(fname, line_content, module_name))

                    if module_name not in imports:
                        imports[module_name] = [full_fname]
                    else:
                        imports[module_name].append(full_fname)

    return imports, scripts, packages


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('codedirs', nargs='+')
    ap.add_argument('--verbose', '-v', action='store_true')
    args = ap.parse_args()

    search_paths = [os.path.abspath(p) for p in args.codedirs]

    all_imports = {}
    all_scripts = {}
    all_packages = set()

    for search_p in search_paths:

        if args.verbose:
            print('Scanning {} for dependencies'.format(search_path))

        imports, scripts, packages = search(search_p, args.verbose)

        all_imports.update(imports)
        all_scripts.update(scripts)
        all_packages = all_packages.union(packages)

    print('Imports:')
    pprint.pprint(all_imports)

    #print('Scripts:')
    #pprint.pprint(all_scripts)

    print('Packages:')
    print(all_packages)

    imports_external, imports_internal, imports_std = classify_imports(all_imports, all_scripts)

    print('\nExternal imports:', imports_external)
    print('\nInternal imports:', imports_internal)
    print('\nStd imports:', imports_std)
