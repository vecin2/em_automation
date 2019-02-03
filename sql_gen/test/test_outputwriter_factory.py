import sys
from sql_gen.outputwriter_factory import OutputWriterFactory

def test_when_dir_passed_outputs_to_file():
    sys.argv=['.','-d','modules/my_module']
    outputwriter=OutputWriterFactory().make()

    assert "modules/my_module" == outputwriter.path

def test_when_no_dir_passed_ouputs_to_screen():
    sys.argv=['.']
    outputwriter=OutputWriterFactory().make()

    assert "console" == outputwriter.type
