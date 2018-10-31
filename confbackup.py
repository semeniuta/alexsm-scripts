"""
Backup Unix configuration files on macOS, Ubuntu, and Raspbian.
Saves the backup in a directory tagged with a timestamp, e.g.
~/confbackup_2018-10-31_080945

The default parent directory (~) can be overriden with the --out parameter

Examples:

python confbackup.py --plaform pi
python confbackup.py --plaform ubuntu --out /dir/to/save
"""

import os
import argparse
import time
import shutil

FILE_MAPPING = dict()

FILE_MAPPING['pi'] = {
    'etc_network_interface': '/etc/network/interfaces',
    'etc_dhcpcd.conf': '/etc/dhcpcd.conf',
    'dot_bashrc': '~/.bashrc',
    'dot_profile': '~/.profile'
}

FILE_MAPPING['ubuntu'] = {
    'etc_network_interface': '/etc/network/interfaces',
    'dot_bashrc': '~/.bashrc',
    'dot_profile': '~/.profile'
}

FILE_MAPPING['mac'] = {
    'dot_bashrc': '~/.bashrc',
    'dot_bash_profile': '~/.bash_profile'
}

def generate_datetime_str():
    return time.strftime("%Y-%m-%d_%H%M%S", time.gmtime())

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(description='Perform backup of config files.')
    arg_parser.add_argument('--out', default='~')
    arg_parser.add_argument('--platform', required=True)
    args = arg_parser.parse_args()

    if args.platform not in FILE_MAPPING.keys():
        print('--platform parameter shoud be one of:')
        for k in FILE_MAPPING.keys():
            print(k)
        exit()

    save_f = 'confbackup_{}'.format(generate_datetime_str())
    save_dir = os.path.join(os.path.expanduser(args.out), save_f)
    print('Backing up to', save_dir)
    os.makedirs(save_dir)

    for f_key, f_loc_str in FILE_MAPPING[args.platform].items():

        f_src = os.path.expanduser(f_loc_str)

        if os.path.exists(f_src):

            print(f_src, '->', f_key)

            f_dst = os.path.join(save_dir, f_key)
            shutil.copyfile(f_src, f_dst)
