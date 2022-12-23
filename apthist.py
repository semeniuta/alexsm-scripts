"""
Parses the apt history log on Ubuntu/Debian (/var/log/apt/history.log)
with different output options.

Use cases:

The `list` action outputs for each entry:
(index, date and time key, invoked command)

python apthist.py list
python apthist.py list --file /path/to/custom/history.log

The `describe` actions provides a detailed description 
of a particular entry indentified by its index from `list`

python apthist.py describe --index 10
python apthist.py describe --index 10 --file /path/to/custom/history.log

The `packages` action prints a list of packages installed (one per line)  
for an entry identified by index from `list`

python apthist.py packages --index 10
"""

import re
import argparse
from pprint import pprint

DEFAULT_FILENAME = '/var/log/apt/history.log'


def find_matches(s, pattern):
    match = re.search(pattern, s)
    return match.groupdict()


def update_entry(entry, line, pattern):
    d = find_matches(line, pattern)
    entry.update(d)


def parse_packages(packages_unparsed):

    res = []

    for s in packages_unparsed.split(')')[:-1]:

        pkg_arch, version_info = s.split('(')

        idx = 0
        if pkg_arch.startswith(','):
            idx = 1

        pkg, arch = pkg_arch.split(' ')[idx].split(':')
        
        res.append((pkg, arch, version_info))
        
    return res
           
                
def parse(fname):

    f = open(fname)

    entries = dict()
    first_time = True

    idx = 0

    for line in f:

        if line.startswith('Start-Date:'):

            if first_time:
                first_time = False
            else:
                entries[idx] = current_entry
                idx += 1

            current_entry = dict()
            update_entry(current_entry, line, '(Start-Date:) (?P<date>.*)')

        elif line.startswith('Commandline:'):

            update_entry(current_entry, line, '(Commandline:) (?P<command>.*)')
        
        elif line.startswith('Requested-By:'):

            update_entry(current_entry, line, '(Requested-By:) (?P<username>[a-zA-Z]+) \((?P<userid>[0-9]+)\)')

        elif line.startswith('Install:') or line.startswith('Upgrade:'):

            packages_match_dict = find_matches(line, '(?P<operation>Install|Upgrade):\s(?P<packages_unparsed>.*)')
           
            current_entry['operation'] = packages_match_dict['operation']
            
            packages_unparsed = packages_match_dict['packages_unparsed']
            current_entry['packages'] = parse_packages(packages_unparsed) 

        else:
            pass

    entries[idx] = current_entry

    return entries


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--file', default=DEFAULT_FILENAME)
    arg_parser.add_argument('action')
    arg_parser.add_argument('--index', type=int)
    args = arg_parser.parse_args()

    entries = parse(args.file)

    if args.action == 'list':
        
        for k in sorted(entries.keys(), reverse=True):
            v = entries[k]
            
            print(k, v['date'])
            
            if 'command' in v:
                print(v['command'])	
            else:
                print('Operation by user', v['username'])
            
            print()

    elif args.action == 'describe':
        if args.index is not None:
            pprint(entries[args.index])
        else:
            print('No index is provided')

    elif args.action == 'packages':
        if args.index is not None:

            # TODO Allow this only for entries with install

            for p, _, _ in entries[args.index]['packages']:
                print(p)

        else:
            print('No index is provided')

    else:
        print('Not valid action')
    
    
    
