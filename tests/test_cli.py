from typer.testing import CliRunner
import pytest

from searcher import app


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
        '--json-file', 'tests/raw data/items_by_character_2020-05-30.json'
    ])

    # THEN the values are correct
    assert result.stdout in [
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbl', ['Ral Rune'])]\n",
        "[('USEast/TestAccount3/TChardr', ['Zod Rune', 'Tal Rune']), ('USEast/TestAccount1/TCharbm', ['Ral Rune'])]\n"
        ]
