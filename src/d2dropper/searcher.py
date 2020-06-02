from collections import Counter
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional, Tuple


def open_file(file_name: Optional[str] = None) -> str:
    """Opens the appropriate droplist file"""
    if file_name is None:
        file_name = 'droplist.txt'

    print(f'Looking for {file_name} in this folder {Path(__file__).parent}')

    with open(Path(file_name)) as output_file:
        print(f'Found droplist!: {file_name}')
        return output_file.read()


def parse_item(item: list) -> dict:
    item_name = item[0][:item[0].find('(')].strip()
    description = item[1:len(item) - 2]

    _character_line = item[-2]
    character = _character_line[:_character_line.find('/{')]
    item_key = _character_line[_character_line.find('{'):_character_line.find('}')]
    return {
        'name': item_name,
        'character': character,
        'description': description,
        'item_key': item_key,
    }


def parse_droplist_for_items_by_char(raw_data: str) -> List[dict]:
    """Creates a list of items that contains a list of the items properties"""
    items = [[line for line in item.split('\n')] for item in raw_data.split('user\n')]
    return [
        parse_item(item)
        for item in items
    ]


def clean(file_name: Optional[str] = None, output_path: Optional[Path] = None) -> None:
    f"""
    CTRL + A all of the items in Lime Drop and save into a text file.

    Creates a items_by_character_{datetime.now().date()}.json file from limedrop.

    **file_name:** Defaults to 'droplist.txt' or uses the values given
    **output_path:** Defaults to current path or uses the value given 
    """
    raw_data = open_file(file_name)
    items = parse_droplist_for_items_by_char(raw_data)

    data = {}
    for item in items:
        item_name = item['name']
        description = item['description']
        character = item['character']

        characters_list = data.get(item_name, {'characters_holding': []}).get('characters_holding')
        new_characters_list = characters_list + [character]

        data[item_name] = {
            'name': item_name,
            'characters_holding': new_characters_list,
            'description': description,
        }

    file_name = f'items_by_character_{datetime.now().date()}.json'
    if output_path:
        file_name = output_path / file_name

    with open(file_name, 'w') as output_file:
        json.dump(data, output_file)
    print(f'outputted to: {file_name}')


def search(items: List[str], json_file: Optional[Path] = None) -> List[Tuple[str, List[str]]]:
    f"""
    Using the items_by_character_YYYY-MM-DD.json file from limedrop's data spits out the 
    accounts and character information of the mules to reduce the number of mules needed to drop the given items.

    **items:** List of items to be searched for

    **The items_by_character file needs to be in the same folder as this exe!**
    """

    def get_json_file(given_file: Optional[Path]) -> Path:
        if given_file and (Path(__file__).parent / Path(given_file)).is_file():
            return Path(Path(__file__).parent / given_file)

        current_directory = Path(__file__).parent
        files_ = list(current_directory.iterdir())

        def get_most_recent_droplist(files: list) -> str:
            files.sort()
            files.reverse()
            for file in files:
                if file.name.startswith('items_by_character_'):
                    return file
            print(f'Could not find the item_by_character file!')

        return get_most_recent_droplist(files_)

    cleaned_droplist = get_json_file(json_file)
    with open(cleaned_droplist) as file_:
        item_map = json.load(file_)

    relevant_items = {
        item: set(item_map.get(item, {'character_holding': []})['characters_holding'])
        for item in items
    }

    results = []

    def find_mule_with_most_items() -> str:
        count = Counter([acct
                         for item in relevant_items.keys()
                         for acct in relevant_items[item]
                         ])
        return count.most_common()[0][0]

    def remove_items_for_(account: str) -> List[str]:
        del_items = []

        # Create a copy so we can delete from the original
        rel_items = relevant_items.copy()

        for item, accounts in rel_items.items():
            if account in accounts:
                del_items += [item]
                del relevant_items[item]

        return del_items

    while relevant_items:
        account_ = find_mule_with_most_items()
        new_items_found = remove_items_for_(account_)

        results += [(account_, new_items_found)]

    return results
