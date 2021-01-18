import sys
from subprocess import check_output
from subprocess import STDOUT
 
 
def run_apt_show(package_name):
    
    cmd = ['apt', 'show', package_name]
    
    out = check_output(cmd, stderr=STDOUT)
    
    return out.split(b'\n')
     
     
if __name__ == '__main__':
    
    package_name = sys.argv[1]
    
    res = run_apt_show(package_name)
    
    for line in res:
        print(line)
