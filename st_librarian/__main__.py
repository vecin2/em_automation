from pathlib import Path

import fire

from st_librarian import DocGenerator, Renamer, SQLTaskLib
from st_librarian.sqltasklib import ViewType


def generate_docs(library):
    library_path = Path(library)
    library = SQLTaskLib(library_path)
    doc_generator = DocGenerator(library)

    doc_generator.generate(library_path / "docs/LibraryByFolder.md", ViewType.BY_FOLDER)
    # doc_generator.generate(library_path / "docs/LibraryByEntity.md",ViewType.BY_ENTITY)


def rename(old_name, new_name, library):
    library_path = Path(library).absolute()
    library = SQLTaskLib(library_path)
    Renamer(library).rename(old_name, new_name)


if __name__ == "__main__":
    fire.Fire({"generate_docs": generate_docs, "rename": rename})
