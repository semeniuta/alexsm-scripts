import sys
from subprocess import check_output
from subprocess import STDOUT
 
 
def run_apt_show(package_name):
    
    cmd = ['apt', 'show', package_name]
    
    out = check_output(cmd, stderr=STDOUT)
    
    return out.split(b'\n')


def get_set(out, prefix):
    
    for line in out:
        if line.startswith(prefix):
            packages = [el.strip().decode('utf-8') for el in line.split(b',')]
            return set(packages)
        
    return set()

    

def compare(out_1, out_2):
    
    dep_1 = get_set(out_1, b'Depends')
    dep_2 = get_set(out_2, b'Depends')
    
    print(dep_1 & dep_2)
     
     
if __name__ == '__main__':
    
    package_1 = sys.argv[1]
    package_2 = sys.argv[2]
    
    out_1 = run_apt_show(package_1)
    out_2 = run_apt_show(package_2)
    
    compare(out_1, out_2)
