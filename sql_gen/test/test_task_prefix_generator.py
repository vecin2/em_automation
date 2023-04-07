import pytest

from sql_gen.commands.create_sql_cmd.task_prefix_generator import \
    TaskPrefixGenerator

# existing_task_folders = sorted(self.parent_folder.iterdir())
# if existing_task_folders:
#     last_folder = existing_task_folders[-1]
test_values = [
    ("015_bla", "016_"),
    ("01_bla", "02_"),
    ("01-bla", "02-"),
    ("01.bla", "02."),
    ("bla", ""),
]


@pytest.mark.parametrize("test_input,expected", test_values)
def test_prefix_generator(test_input, expected):
    path = "/mnt/c/em/projects/DU/du/modules/DuConfiguration/sqlScripts/oracle/updates/Du_01"
    prefix_generator = TaskPrefixGenerator()
    result = prefix_generator.next(test_input)
    assert expected == result
