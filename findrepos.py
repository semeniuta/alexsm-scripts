import os
import argparse
import subprocess

BOLD = '\033[1m'
GREEN = '\033[92m'
PURPLE = '\033[95m'
END = '\033[0m'


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('root_dir')

    return parser.parse_args()


def git_status(path, root_dir):

    os.chdir(path)
    result = subprocess.run(['git', 'status', '--short'], capture_output=True)

    relative_path = path.split(root_dir)[-1][1:]

    if result.stdout == b'':
        print(relative_path, end=': ')
        print(f'{GREEN}OK{END}')
    else:
        lines = result.stdout.strip().split(b'\n')
        print(f'{BOLD}{relative_path}{END}:')
        for line in lines:
            print(f' -> {PURPLE}{line.decode().strip()}{END}')


def main():

    working_dir = os.getcwd()
    args = parse_args()

    dirs_with_git_repos = []
    for root, dirs, _ in os.walk(args.root_dir):
        if '.git' in dirs:
            dirs_with_git_repos.append(root)

    os.chdir(working_dir)

    for repo_root in dirs_with_git_repos:
        git_status(repo_root, args.root_dir)


if __name__ == '__main__':
    main()
