class CreateDocumentFromTemplateCommand(object):
    def run(self):
        return  "hello Mark"

class CreateDocumentFromMultipleTemplatesCommand(object):
    def __init__(self,doc_creator=None):
        self.doc_creator=doc_creator
    """It fills one or multiple templates and returns and output string"""
    def run(self):
        result =""
        str_document = self.doc_creator.run()
        while str_document is not None:
            if result is not "":
                result +="\n"
            result +=str_document
            str_document = self.doc_creator.run()
        return result

class FillMultipleTemplatesDisplayer(object):
    """displayer which request information for filling multiple tempaltes"""
    def ask_to_select_a_template():
        """"""

