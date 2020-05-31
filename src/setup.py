from pathlib import Path
import setuptools


with open(Path('d2dropper/VERSION'), 'r') as version_file:
    version = version_file.read().strip()


with open(Path('../readme.md'), 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name="d2dropper",
    version=version,
    author="Daniel Butler",
    description="Command Line and GUI tool add on for d2's lime dropper",
    url="https://github.com/daniel-butler/d2dropper",
    packagers=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows 10",
    ],
    python_requires='>=3.7',

)

