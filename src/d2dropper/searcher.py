from collections import Counter, namedtuple
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional, Tuple

import networkx as nx


Item = namedtuple('Item', 'name character description key')


def open_file(file_name: Optional[str] = None) -> str:
    """Opens the appropriate droplist file"""
    if file_name is None:
        file_name = 'droplist.txt'

    print(f'Looking for {file_name} in this folder {Path(__file__).parent}')

    with open(Path(file_name)) as output_file:
        print(f'Found droplist!: {file_name}')
        return output_file.read()


def parse_item(item: list) -> Item:
    item_name = item[0][:item[0].find('(')].strip()
    description = item[1:len(item) - 2]

    _character_line = item[-2]
    character = _character_line[:_character_line.find('/{')]
    item_key = _character_line[_character_line.find('{'):_character_line.find('}')]
    return Item(
        name=item_name,
        character=character,
        description=description,
        key=item_key,
    )


def parse_droplist_for_items_by_char(raw_data: str) -> List[Item]:
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
        characters_list = data.get(item.name, {'characters_holding': []}).get('characters_holding')
        new_characters_list = characters_list + [item.character]

        data[item.name] = {
            'name': item.name,
            'characters_holding': new_characters_list,
            'description': item.description,
        }

    file_name = f'items_by_character_{datetime.now().date()}.json'
    if output_path:
        file_name = output_path / file_name

    with open(file_name, 'w') as output_file:
        json.dump(data, output_file)
    print(f'outputted to: {file_name}')


def create_graph(find_items: List[str], file_name: Optional[str] = None) -> nx.Graph:
    """Creates Graph of characters holding each item"""
    raw_data = open_file(file_name)
    items = parse_droplist_for_items_by_char(raw_data)
    graph = nx.Graph()
    graph.add_nodes_from([item.name for item in items if item.name in find_items], bipartite=0)
    graph.add_nodes_from([item.character for item in items if item.name in find_items], bipartite=1)
    graph.add_edges_from([(item.name, item.character, {'key': item.key}) for item in items if item.name in find_items])
    return graph


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
