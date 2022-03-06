import sys
import subprocess

def run_command(cmd, suffix):    
    out = subprocess.check_output([cmd, suffix], stderr=subprocess.STDOUT)
    elements = filter(lambda s: len(s) > 0, out.split(b'\n'))
    return tuple(map(lambda s: s.decode('UTF-8'), elements))

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit(-1)

    pkg_name = sys.argv[1]

    deps = set((pkg_name, ) + run_command('./depends-recommends.sh', pkg_name))

    for d in deps:
        res = run_command('./rdepends.sh', d)
        outside = set(res) - deps
        if (len(outside) == 0):
            print(f'{d}')
    
