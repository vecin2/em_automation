from sql_gen.create_doc_from_multiple_templates_command import CreateDocumentFromMultipleTemplatesCommand
from sql_gen.create_document_from_template_command import CreateDocumentFromTemplateCommand
from unittest import mock as mocker


def make(ouput):
    doc_creator=mocker.Mock(spec=CreateDocumentFromTemplateCommand)
    doc_creator.run.side_effect=ouput
    return CreateDocumentFromMultipleTemplatesCommand(doc_creator)

def test_when_one_template_filled():
    class_under_test=make(["hello",None])

    assert "hello" == class_under_test.run()

def test_when_multiple_templates_filled_combines_them_into_a_doc(mocker):
    class_under_test=make(["hello","hello", None])

    assert "hello\nhello" == class_under_test.run()
