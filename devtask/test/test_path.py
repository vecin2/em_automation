from devtask.extend_process import extend_process
import os
import pathlib
import shutil
import pytest

from sql_gen.app_project import AppProject
from sql_gen.emproject import EMProject
import devtask.extend_process

def Path(path):
    return pathlib.Path(path)

testfilesystem =Path(os.path.dirname(__file__))/ ".testfilesystem"

def clear_testfilesystem():
    if testfilesystem.exists():
        shutil.rmtree(testfilesystem)
    #os.rmdir(testfilesystem)

clear_testfilesystem()

def create_file(path,contents=None):
    finalpath = fullpath(path)
    os.makedirs(os.path.dirname(finalpath), exist_ok=True)
    with open(finalpath,"w+") as f:
        f.write(contents)
    return finalpath

def fullpath(relativepath):
    return testfilesystem / relativepath


@pytest.mark.skip
def test_something(capsys):
    classpath="CoreEntities/InvalidProcess.xml"
    relative_src="opt/em/products/agent_desktop/repository/default/"+classpath
    src =create_file(relative_src,contents="hola")
    em_prj_path="/home/dgarcia/dev/python/em_automation/devtask/test/..testfilesystem/opt/em/projects/pacificorp"
    app_project = EMProject(emprj_path=em_prj_path)
    product_path="/home/dgarcia/dev/python/em_automation/devtask/test/.testfilesystem/opt/em/products/agent_desktop"
    app_project._config={"product.home":product_path}
    #assert "guaje" == app_project.product_layout()['repo_modules'].path
    em_prj_path="/home/dgarcia/dev/python/em_automation/devtask/test/.testfilesystem/opt/em/projects/pacificorp"
    devtask.extend_process.app_project = AppProject(emprj_path=em_prj_path)
    product_path="/home/dgarcia/dev/python/em_automation/devtask/test/.testfilesystem/opt/em/products/agent_desktop"
    app_project.emproject._config={"product.home":product_path}
    app_project._em_config={"product.home":product_path}
    extend_process(classpath)
    assert os.path.exists(src)
    assert capsys.readouterr().out == "dd"
