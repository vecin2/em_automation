from st_librarian import DocGenerator, SQLTaskLib
from st_librarian.sqltasklib import ViewType


class GenerateLibDocsCommand(object):
    def __init__(self, library_path):
        self.library_path = library_path

    def run(self):
        return self.generate_docs(self.library_path)

    def generate_docs(self,library):
        library_path = library
        library = SQLTaskLib(library_path)
        doc_generator = DocGenerator(library)

        doc_generator.generate(
            library_path / "docs/LibraryByFolder.md", ViewType.BY_FOLDER
        )
