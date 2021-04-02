import os
import sys
import pytest
import pathlib
import shutil
from io import StringIO

import lxml.etree as ET
from lxml import objectify

from devtask.extend_process import extend_process, main
from devtask.object_factory import new_process_def


def Path(path):
    return pathlib.Path(path)


testfilesystem = Path(os.path.dirname(__file__)) / ".testpath"


class AppRunner(object):
    def __init__(self, capsys):
        self.capsys = capsys
        self.original_stdin = sys.stdin
        self.inputs = []
        if testfilesystem.exists():
            shutil.rmtree(testfilesystem)

    def extend_process(self, src, dst=None):
        sys.argv = []
        sys.argv.append("")
        sys.argv.append("extend_process")
        sys.argv.append(str(src))
        if dst:
            sys.argv.append(str(dst))

        str_inputs = "\n".join([input for input in self.inputs])
        sys.stdin = StringIO(str_inputs)
        try:
            result = main()
            self.inputs = []
        except Exception as exception:
            self.inputs = []
            raise exception

    def user_inputs(self, user_input):
        self.inputs.append(user_input)
        return self

    def teardown(self):
        sys.stdin = self.original_stdin

    def displays_message(self, message):
        assert self.capsys.readouterr().out == message

    def assert_file_exists(self, filepath, contents):
        abspath = fullpath(str(filepath.replace(".", os.sep)) + ".xml")
        abspath = testfilesystem / abspath
        if not abspath.exists():
            assert False, "'" + str(abspath) + "' does not exists"
        assert contents == str(abspath.read_text())


@pytest.fixture
def app_runner(capsys):
    app_runner = AppRunner(capsys)
    yield app_runner
    app_runner.teardown()


@pytest.mark.skip
def test_returnserror_when_invalid_path(app_runner):
    src = Path("Account/NonExitingProcess.xml")
    app_runner.extend_process(src)
    app_runner.displays_message("No process found under '" + str(src) + "'\n")


@pytest.mark.skip
def test_returns_error_when_file_not_a_process(app_runner):
    src = Path("CoraeEntities2/Implementation/Customer/Processes/InvalidProcess.xml")

    src = create_file(str(src), contents="Invalid xml")
    app_runner.extend_process(src)
    app_runner.displays_message(
        "Not a valid xml process found under '" + str(src) + "'\n"
    )


def create_file(path, contents=None):
    finalpath = fullpath(path)
    os.makedirs(os.path.dirname(finalpath), exist_ok=True)
    with open(finalpath, "w+") as f:
        f.write(contents)
    return finalpath


def fullpath(relativepath):
    return testfilesystem / relativepath


@pytest.mark.skip
def test_extend_process_by_copy_copies_process_to_project_path(app_runner):
    source_content = new_process_def()
    src = create_file("CoreEntities/EmptyProcess.xml", contents=source_content)
    dst = fullpath("PRJEntities/Account")
    app_runner.extend_process(src, dst)
    app_runner.assert_file_exists(
        "PRJEntities.Account.EmptyProcess", contents=source_content
    )


@pytest.mark.skip
def test_extend_process_override_dst_if_user_confirms(app_runner, fs):
    source_content = new_process_def()
    src = Path("/repository/default/CoreEntities/EmptyProcess.xml")
    fs.create_file(str(src), contents=source_content)
    dst = Path("/repository/default/PRJEntities/Account")
    fs.create_file(str(dst / "EmptyProcess.xml"), contents="old content")

    app_runner.user_inputs("n").extend_process(src, dst)

    app_runner.assert_file_exists(dst / "EmptyProcess.xml", contents="old content")

    app_runner.user_inputs("y").extend_process(src, dst)

    app_runner.assert_file_exists(dst / "EmptyProcess.xml", contents=source_content)


@pytest.mark.skip
def test_when_no_dst_provided_prompts_for_dst(app_runner, fs):
    source_content = new_process_def()
    src = Path("/repository/default/CoreEntities/EmptyProcess.xml")
    fs.create_file(str(src), contents=source_content)

    dst = Path("/repository/default/PRJEntities/Account2")
    app_runner.user_inputs(str(dst)).extend_process(src)

    app_runner.assert_file_exists(dst / "EmptyProcess.xml", contents=source_content)


@pytest.mark.skip
def test_when_enter_blank_on_dst_prompt_it_uses_default(app_runner, fs):
    create_config({"project.prefix": "MP"})
    source_content = new_process_def()
    src = Path("/repository/default/CoreEntities/EmptyProcess.xml")
    fs.create_file(str(src), contents=source_content)

    dst = Path("/repository/default/PRJEntities/Account2")
    app_runner.user_inputs("\n").extend_process(src)

    app_runner.assert_file_exists(dst / "EmptyProcess.xml", contents=source_content)
