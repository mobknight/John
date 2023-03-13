import json
from collections.abc import MutableMapping
import os
from pathlib import Path
from datetime import datetime
import argparse


def read_json(file):
    with open(file, 'r') as f:
        try:
            data: dict = json.load(f)
            return data
        except:
            print('Error while reading file {}. You sure you got the right json file?'.format(file))


def flatten_json(data, parent_key='', sep='.'):
    # Nested json 처리
    items = []
    for key, value in data.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def find_discrepancies(lst):
    discrepancies: dict = {}
    for key, value in lst[0]['data'].items():
        for component in lst[1:]:
            if key not in component['data']:
                if key not in discrepancies:
                    discrepancies[key] = {}
                discrepancies[key][component['name']] = 'Key Does Not Exist.'
            else:
                if value != component['data'][key]:
                    if key not in discrepancies:
                        discrepancies[key] = {}
                    discrepancies[key][lst[0]['name']] = value
                    discrepancies[key][component['name']] = component['data'][key]
                component['data'].pop(key)
    
    for component in lst[1:]:
        for key, value in component['data'].items():
            if key not in discrepancies:
                discrepancies[key] = {}
            discrepancies[key][component['name']] = value
    
    return discrepancies


def get_json_files_from_dir(dir):
    dic = {}
    pathlist = Path(dir).rglob('*.json')
    for path in pathlist:
        if os.path.isfile(path):
            path_in_str = str(path)
            relpath_in_str = str(os.path.relpath(path, dir)) # Relative Path로 찾아오기
            dic[relpath_in_str] = path_in_str
    return dic


def compare_json_files(files):
    lst = []
    for item in files:
        raw_data = read_json(item['file'])
        data = flatten_json(raw_data)
        lst.append({
            'name': item['group'],
            'data': data
        })
    discrepancies = find_discrepancies(lst)
    return discrepancies


def write_output(comparison, discrepancies, output_file):
    result = {
        comparison: discrepancies
    }
    with open(output_file, 'a') as f:
        f.write(json.dumps(result, indent=4, sort_keys=True))
        f.write(',\n')


def sign_off(output_file):
    with open(output_file, 'a') as f:
        f.write('\n\n{"Job Done": "' + datetime.today().strftime("%Y/%m/%d %H:%M:%S") + '"}]')


def select_mode(lst):
    file_mode = False
    dir_mode = False
    
    for target in lst:
        if Path(target).is_file():
            file_mode = True
        elif Path(target).is_dir():
            dir_mode = True
        else:
            return '\n---- Error: {} is neither file nor directory.\n'.format(target)

    if file_mode == dir_mode:
        return '\n---- Error: Source and target(s) should be equivalent.\n'
    elif file_mode == True and dir_mode == False:
        return 'file'
    elif file_mode == False and dir_mode == True:
        return 'dir'
    

def main(a, b, output_file):
    mode: str = ''
    print('\n=-=-=-= Finding discrepancies between {} and {}...'.format(a, b))
    lst = []
    lst.append(a)
    lst.extend(b)
    
    # 주어진 A, B가 파일인지 디렉토리인지 판별하여 모드 설정하기
    mode = select_mode(lst)
    if mode not in ['file', 'dir']:
        print(mode)
        return None

    # Output 파일 초기화
    with open(output_file, 'w') as f:
        f.write('[\n')
    
    files = []
    
    # 파일 모드인 경우, 비교 1회 수행하고 종료
    if mode == 'file':
        print('---- Running in Files Mode...')
        for file in lst:
            files.append({
                'group': file,
                'file': file
            })
        result = compare_json_files(files)
        s = ', '.join([str(item) for item in lst])
        write_output(s, result, output_file)
        sign_off(output_file)
        print('\n=-=-=-= Job Done =-=-=-=\n')
        return None
    
    # 디렉토리 모드인 경우, A 하위 경로의 모든 JSON 파일을 찾아 동일 경로에 동일 파일이 비교 대상(B, C, D...) 경로에도 존재하면 비교.
    # A에만, 혹은 비교 대상(B, C, D...)에만 존재하는 파일의 경우 아예 비교하지 않음. 따라서 결과에서도 제외됨.
    if mode == 'dir':
        print('---- Running in Directories Mode...')
        for dir in lst:
            files.append({
                'group': dir,
                'files': get_json_files_from_dir(dir)
            })
        
        for key, value in files[0]['files'].items():
            compared_lst = [{
                'group': files[0]['group'],
                'file': value
            }]
            for target in files[1:]:
                if key in target['files'].keys():
                    compared_lst.append({
                        'group': target['group'],
                        'file': target['files'][key]
                    })
            result = compare_json_files(compared_lst)
            write_output(key, result, output_file)

        sign_off(output_file)
        print('\n=-=-=-= Job Done. Check your Output in {} =-=-=-=\n'.format(output_file))


def cli():
    parser = argparse.ArgumentParser(description='Find discrepancies in JSON Files!\nMade with Python 3.10.10 with default libraries only, but will probably run on 3.5+\nJohn Lee, 2023', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', type=str, help='AKA "A". Can be a file or directory.')
    parser.add_argument('target', type=str, nargs='+', help='AKA "B, C, D...". Should be equivalent to A.')
    parser.add_argument('-o', '--output', type=str, required=False, default='output.json', help='Output file name (in JSON). Default is ./output.json.')

    args = parser.parse_args()

    main(args.source, args.target, args.output)


cli()