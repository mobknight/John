# Created in 2020.12 during KB Life Digital Platform 2.0 Project (PaaS + Gitlab + MSA)
# To go in each subdirectory and run git commands

import os
import sys
import subprocess

def getArgs():
    print('')
    if len(sys.argv) < 3:
        print('======== Error: path and command not found')
        sys.exit()
    if not os.path.exists(sys.argv[1]):
        print('======== Error: path not exist')
        sys.exit()
    if sys.argv[2].lower() == 'git':
        del sys.argv[2]
    
    print('======== Running git : ', sys.argv[2:], ' in subfolders of ', sys.argv[1])
    valid = {'y': True, 'yes': True, 'n': False, 'no': False}
    print("======== Continue? [y/n]")
    choice = input().lower()
    if choice == '':
        sys.exit()
    else:
        if valid[choice] == False:
            sys.exit()
    return sys.argv[1:]

def main(given_path, commands):
    sub_folders = next(os.walk(given_path))
    for f in sub_folders[1]:
        f_fullpath = os.path.join(given_path, f)
        runGit(f_fullpath, commands)

def runGit(path, *arguments):
    lst = ['git', '-C', path]
    for arg in arguments:
        if type(arg) is list:
            lst.extend(arg)
        else:
            lst.append(arg)
    print('\n======== Running git commands in ', path)
    subprocess.run(lst)

args = getArgs()
main(args[0], args[1:])