from pathlib import Path

from typer.testing import CliRunner
import pytest

from d2dropper.cli import app


def test_cli_command_works_as_expected(tmp_path):
    # GIVEN a runner
    runner = CliRunner()

    # WHEN invoking the cli
    result = runner.invoke(
        app, ['clean', '--file-name', 'tests/raw data/droplist.txt', '--output-path', str(tmp_path)]
    )

    # THEN the tmp_path has the expected file
    assert len(list(tmp_path.iterdir())) == 1

    # THEN the json file is as expected
    pytest.fail('not completed')


def test_find_items():
    # GIVEN a runner
    runner = CliRunner()

    # When searching
    result = runner.invoke(app, [
        'search',
        'Zod Rune', 'Tal Rune', 'Ral Rune',
        '--json-file', str(Path(__file__).parent / 'raw data/items_by_character_2020-05-30.json')
    ])

    # THEN the values are correct
    assert result.stdout in [
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbh', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbi', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbj', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbk', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbl', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbm', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbn', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbi', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount2/TCharcc', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount3/TChardh', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount3/TChardl', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount3/TChardk', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount6/TChargj', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount7/TCharhb', ['Ral Rune'])]\n",
        ]
