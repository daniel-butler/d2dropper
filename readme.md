## QuickStart

First get the items from lime dropper save it as  `droplist.txt` file next to the `.exe` file

```bash
dropper.exe clean

# or explore the other options with
dropper.exe clean --help
```

**Search for items to get the best characters for the items when you have a `items_by_character_*.json` file!**

![Search for Items](docs/search-video.gif)


## Developing

```bash
# Install the requirements
python -m pip install -r requirements.txt

# create the exe with pyinstaller and the following commands
pyinstaller searcher.py -n dropper -F --hidden-import=pkg_resources.py2_warn
```

Error with setup tools that requires the hidden-import command line argument
https://github.com/pypa/setuptools/issues/1963
