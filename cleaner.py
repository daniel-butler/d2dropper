from datetime import datetime
from pathlib import Path

import json


# Read the file
print(f'Looking for droplist.txt in this folder {Path(__file__).parent}')
with open('droplist.txt') as output_file:
    raw_data = output_file.read()

print('Found droplist!')

# breakout the items into a list
items = [[line for line in item.split('\n')] for item in raw_data.split('user\n')]


# put the items into a dictionary
def get_data() -> dict:
    data = {}
    for item in items:
        item_name = item[0][:item[0].find('(')].strip()
        description = item[1:len(item) - 2]

        character_line = item[-2]
        character = character_line[:character_line.find('/{')]
        item_key = character_line[character_line.find('{'):character_line.find('}')]

        characters_list = data.get(item_name, {'characters_holding': []}).get('characters_holding')
        new_characters_list = characters_list + [character]

        data[item_name] = {
            'name': item_name,
            'characters_holding': new_characters_list,
            'description': description,
        }
    return data


filename = f'items_by_character_{datetime.now().date()}.json'
with open(filename, 'w') as output_file:
    json.dump(get_data(), output_file)

print(f'outputted to: {filename}')


def test_get_data():
    get_data()


