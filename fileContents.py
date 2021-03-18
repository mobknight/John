# John Lee Works
# Created in 2020.12 during KB Life Digital Platform 2.0 Project (PaaS + Gitlab + MSA)
# To replace URL string in certain files in all subdirectories
# Version 1.4

from pathlib import Path
import sys
import os
import re

def main():
    file_path, file_name, mode, input_type = getCommandInfo()
    file_list = getFilesFromDir(file_path, file_name)
    print("\n".join(file_list))
    print('======== Found', len(file_list), 'files.')
    strings = getStrings(mode, input_type)
    done_files = 0
    for file in file_list:
        if mode == 'r':
            done_files += doReplace(file, strings[0], strings[1], input_type)
        elif mode == 'd':
            done_files += doDelete(file, strings[0], input_type)
        elif mode == 'i':
            done_files += doInsert(file, strings[0], strings[1], input_type)
        elif mode == 'a':
            done_files += doAppend(file, strings[0], strings[1])
        elif mode == 'f':
            done_files += doFind(file, strings[0], input_type)
        elif mode == 'e':
            done_files += doEncode(file, strings[0], strings[1])
    print('\n======== Finished Job for :', done_files, 'files')

def getCommandInfo():
    lst = sys.argv

    if len(lst) > 1:
        file_path = str(lst[1])
    else:
        file_path = input('======== Path : ')
    if not os.path.exists(file_path):
        print('======== Error: path not exist')
        sys.exit()
    
    if len(lst) > 2:
        file_name = str(lst[2])
    else:
        file_name = input('======== File Name (* for any) : ')
    
    if len(lst) > 3:
        mode = str(lst[3])
    else:
        print('======== Select Mode\n  r : Replace\n  d : Delete line\n  i : Insert line\n  a : Append line\n  f : Find files (and do nothing)\n  e : change Encoding')
        mode = input('======== [ r / d / i / a / f / e ]: ')
    valid_mode = ('r', 'd', 'i', 'a', 'f', 'e')
    checkIfValid(mode, valid_mode)

    if len(lst) > 4:
        if lst[4].lower() == 'regex':
            input_type = 'RegEx'
        else:
            input_type = 'String'
    else:
        if mode in ('r', 'd', 'i', 'f'):
            s = input('======== Type "regex" to enable Regular Expression mode : ')
            if s.lower() == 'regex':
                input_type = 'RegEx'
            else:
                input_type = 'String'
        else:
            input_type = 'String'
    
    return file_path, file_name, mode, input_type

def checkIfValid(str_input, valid):
    str_input = str(str_input).lower()
    if str_input == '':
        sys.exit()
    else:
        if str_input not in valid:
            print('======== Invalid input. Valid inputs are : ', valid, '\nExiting... \n')
            sys.exit()

def getFilesFromDir(dir, filename):
    lst = []
    pathlist = Path(dir).rglob(filename)
    for path in pathlist:
        if os.path.isfile(path):
            path_in_str = str(path)
            lst.append(path_in_str)
    return lst

def getStrings(mode, input_type):
    strings = []
    if mode == 'r':
        strings.append(input('======== {} to find : '.format(input_type)))
        strings.append(input('======== String to replace with : ')) # Tried using repr(), turns out it also prints the quotation marks around
        print('\n==== Replacement in place......')
    elif mode == 'd':
        strings.append(input('======== {} in the lines to delete : '.format(input_type)))
        print('\n==== Delete in place......')
    elif mode == 'i':
        strings.append(input('======== {} to find : '.format(input_type)))
        print('======== Lines to insert after the found strings (Press Enter for EOF) : ')
        strings.append(defineLines())
        print('\n==== Insert in place......')
    elif mode == 'a':
        if input_type == 'RegEx':
            print('======== RegEx does not work in Append mode.')
        print('======== Lines to append (Press Enter for EOF) : ')
        strings.append(defineLines())
        strings.append(input('======== Location to append the line to [ t: top / b: bottom ] : '))
        checkIfValid(strings[1], ('t', 'b'))
        print('\n==== Append in place......')
    elif mode == 'f':
        strings.append(input('======== {} to find in the files : '.format(input_type)))
        print('\n==== Find in place......')
    elif mode == 'e':
        strings.append(input('======== Encoding from (default: euc-kr) : '))
        if strings[0] == '': strings[0] = 'euc-kr'
        strings.append(input('======== Encoding to (default: utf-8) : '))
        if strings[1] == '': strings[1] = 'utf-8'
        print('======== Change all file encoding from', strings[0], 'to', strings[1])
        strings.append(input('         [ y / n ] : '))
        checkIfValid(strings[2], ('y', 'yes'))
        print('\n==== Encoding change in place........')
    
    if strings[0] == '':
        print('==== Nothing to find.')
        sys.exit()
    return strings

def defineLines():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)
    return text

def doReplace(given_file, str_before, str_after, input_type):
    count = 0
    result = 0
    if input_type == 'RegEx':
        regex = re.compile(str_before)
    try:
        with open(given_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for n, line in enumerate(lines):
                if input_type == 'String':
                    if str_before in line:
                        line = line.replace(str_before, str_after)
                        count += 1
                        lines[n] = line
                elif input_type == 'RegEx':
                    if re.search(regex, line):
                        matches = re.findall(regex, line)
                        for match in matches:
                            line = line.replace(match, str_after)
                            count += 1
                        lines[n] = line
        with open(given_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        if count > 0:
            print('==== Replaced', count, 'lines in', str(given_file))
            result = 1
    except UnicodeDecodeError:
        print('-------- UnicodeDecodeError on', given_file)
    return result

def doDelete(given_file, str_to_remove, input_type):
    result = 0
    if input_type == 'RegEx':
        regex = re.compile(str_to_remove)
    try:
        with open(given_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            newlines = []
            for line in lines:
                if input_type == 'String':
                    if str_to_remove not in line:
                        newlines.append(line)
                elif input_type == 'RegEx':
                    if re.search(regex, line):
                        pass
                    else:
                        newlines.append(line)
        with open(given_file, 'w', encoding='utf-8') as f:
            f.writelines(newlines)
        count = len(lines) - len(newlines)
        if count > 0:
            print('==== Deleted', count, 'lines in', str(given_file))
            result = 1
    except UnicodeDecodeError:
        print('-------- UnicodeDecodeError on', given_file)
    return result

def doInsert(given_file, str_before, str_to_insert, input_type):
    count = 0
    result = 0
    if input_type == 'RegEx':
        regex = re.compile(str_before)
    try:
        with open(given_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for n, line in enumerate(lines):
                if input_type == 'String':
                    if str_before in line:
                        lines.insert(n + 1, str_to_insert + '\n')
                        count += 1
                elif input_type == 'RegEx':
                    if re.search(regex, line):
                        lines.insert(n + 1, str_to_insert + '\n')
                        count += 1
        with open(given_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        if count > 0:
            print('==== Inserted', count, 'lines in', str(given_file))
            result = 1
    except UnicodeDecodeError:
        print('-------- UnicodeDecodeError on', given_file)
    return result

def doAppend(given_file, str_to_append, append_location):
    locations = {'t': 'top', 'b': 'bottom'}
    try:
        with open(given_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(given_file, 'w', encoding='utf-8') as f:
            if append_location == 't':
                f.write(str_to_append)
                f.write('\n')
                f.writelines(lines)
            elif append_location == 'b':
                f.writelines(lines)
                f.write('\n')
                f.write(str_to_append)
        print('==== Appended the line in ', str(given_file), 'at the', locations[append_location])
    except UnicodeDecodeError:
        print('-------- UnicodeDecodeError on', given_file)
    return 1

def doFind(given_file, str_to_find, input_type):
    count = 0
    result = 0
    if input_type == 'RegEx':
        regex = re.compile(str_to_find)
    try:
        with open(given_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if input_type == 'String':
                    if str_to_find in line:
                        count += 1
                elif input_type == 'RegEx':
                    if re.search(regex, line):
                        count += 1
        if count > 0:
            print('==== Found', count, 'lines in', str(given_file))
            result = 1
    except UnicodeDecodeError:
        pass
    return result

def doEncode(given_file, encoding_from, encoding_to):
    result = 0
    try:
        with open(given_file, 'r', encoding=encoding_from) as f:
            lines = f.readlines()
        with open(given_file, 'w', encoding=encoding_to) as f:
            f.writelines(lines)
        print('==== Changed file encoding from', encoding_from, 'to', encoding_to, 'for', str(given_file))
        result = 1
    except UnicodeDecodeError:
        print('-------- UnicodeDecodeError on', str(given_file))
    return result

main()