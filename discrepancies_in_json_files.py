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


def flatten(data, parent_key='', sep='.'):
    # Nested json 처리
    items = []
    for key, value in data.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def find_discrepancies(data1, data2):
    discrepancies: dict = {}
    for key, value in data1.items():
        if key in data2:
            try:
                if data1[key] != data2[key]:
                    discrepancies[key] = {
                        'A': data1[key],
                        'B': data2[key]
                    }
                data2.pop(key)
            except:
                print('Error while comparing {} and {}'.format(data1, data2))
        else:
            discrepancies[key] = {
                'A': data1[key],
                'B': 'Key Does Not Exist.'
            }
    for key, value in data2.items():
        discrepancies[key] = {
            'A': 'Key Does Not Exist.',
            'B': data2[key]
        }
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


def compare_json_files(file1, file2):
    print('\n---- Comparing {} and {}...'.format(file1, file2))
    data = read_json(file1)
    data1 = flatten(data)
    data = read_json(file2)
    data2 = flatten(data)
    discrepancies = find_discrepancies(data1, data2)
    print('===> Discrepancies: {}'.format(discrepancies))
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


def main(a, b, output_file):
    mode: str = ''
    a = a.strip()
    b = b.strip()
    print('\n=-=-=-= Finding discrepancies between {} and {}...'.format(a, b))
    
    # 주어진 A, B가 파일인지 디렉토리인지 판별하여 모드 설정하기
    if Path(a).is_file() and Path(b).is_file():
        mode = 'file'
    elif Path(a).is_dir() and Path(b).is_dir():
        mode = 'dir'
    else:
        print('\n---- Error: A and B should be equivalent.\n')
        return None

    # Output 파일 초기화
    with open(output_file, 'w') as f:
        f.write('[\n')
    
    # 파일 모드인 경우, 비교 1회 수행하고 종료
    if mode == 'file':
        print('---- Running in Files Mode...')
        result = compare_json_files(a, b)
        write_output(a + ' and ' + b, result, output_file)
        sign_off(output_file)
        print('\n=-=-=-= Job Done =-=-=-=\n')
        return None
    
    # 디렉토리 모드인 경우, A 하위 경로의 모든 JSON 파일을 찾아 동일 경로에 동일 파일이 B 경로에도 존재하면 비교.
    # A 혹은 B에만 존재하는 파일의 경우 아예 비교하지 않음. 따라서 결과에서도 제외됨.
    if mode == 'dir':
        print('---- Running in Directories Mode...')
        a_files = get_json_files_from_dir(a)
        b_files = get_json_files_from_dir(b)
        
        for key in a_files:
            if key in b_files:
                result = compare_json_files(a_files[key], b_files[key])
                write_output(key, result, output_file)
        sign_off(output_file)

# main(a='./no_tracking/test.json', b='./no_tracking/test2.json', output_file='./no_tracking/output.json')  # 파일단위 비교 예시
# main(a='./no_tracking/json_test1', b='./no_tracking/json_test2', output_file='./no_tracking/output.json')   # 디렉토리단위 비교 예시


def cli():
    parser = argparse.ArgumentParser(description='Find discrepancies in JSON Files!\nMade with Python 3.10.10 with default libraries only, but will probably run on 3.5+\nJohn Lee, 2023', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', type=str, help='Called A. Can be a file or directory.')
    parser.add_argument('target', type=str, help='Called B. Should be equivalent to A.')
    parser.add_argument('-o', '--output', type=str, required=False, default='output.json', help='Output file name (in JSON). Default is ./output.json.')

    args = parser.parse_args()

    main(args.source, args.target, args.output)


cli()