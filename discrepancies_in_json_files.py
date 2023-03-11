import json
from collections.abc import MutableMapping

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

def main(file1, file2, output_file):
    print('\n---- Comparing {} and {}...'.format(file1, file2))
    data = read_json(file1)
    data1 = flatten(data)
    data = read_json(file2)
    data2 = flatten(data)
    discrepancies = find_discrepancies(data1, data2)
    print('===> Discrepancies: {}'.format(discrepancies))
    with open(output_file, 'w') as f:
        f.write(json.dumps(discrepancies, indent=4, sort_keys=True))
    print('\n=-=-=-= Job Done =-=-=-=')


main(file1='./no_tracking/test.json', file2='./no_tracking/test2.json', output_file='./no_tracking/output.json')