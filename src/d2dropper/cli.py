from datetime import datetime
from pathlib import Path
from typing import Optional, List

import typer

from . import searcher

app = typer.Typer()


@app.command()
def clean(file_name: Optional[str] = None, output_path: Optional[Path] = None) -> None:
    f"""
    CTRL + A all of the items in Lime Drop and save into a text file.

    Creates a items_by_character_{datetime.now().date()}.json file from limedrop.

    **file_name:** Defaults to 'droplist.txt' or uses the values given
    **output_path:** Defaults to current path or uses the value given 
    """
    searcher.clean(file_name, output_path)


@app.command()
def search(items: List[str], json_file: Optional[Path] = None) -> None:
    f"""
    Using the items_by_character_YYYY-MM-DD.json file from limedrop's data spits out the 
    accounts and character information of the mules to reduce the number of mules needed to drop the given items.

    **items:** List of items to be searched for

    **The items_by_character file needs to be in the same folder as this exe!**
    """
    results = searcher.search(items, json_file)
    typer.echo(results)


if __name__ == '__main__':
    app()
