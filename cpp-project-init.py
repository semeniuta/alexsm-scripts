# Create directory structure of a C++ project
# Influenced by:
# http://hiltmon.com/blog/2013/07/03/a-simple-c-plus-plus-project-structure/

from __future__ import print_function

import os

dirs = [
    'src',
    'include',
    'bin',
    'lib',
    'build',
    'python',
    'test',
    'spike',
    'ide',
    'ide/xcode'
]

if __name__ == '__main__':

    for d in dirs:
        if not os.path.exists(d):
            print('Creating {}'.format(d))
            os.makedirs(d)
        else:
            print('Directory {} alredy exists'.format(d))
