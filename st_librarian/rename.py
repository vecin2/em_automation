from st_librarian import DocGenerator


class Renamer(object):
    def __init__(self, tasklib):
        self.tasklib = tasklib

    def rename(self, old_name, new_name):
        print(f"old_name:{old_name}, new_name:{new_name}")
        references = []
        for template in self.tasklib.list_all():
            if old_name in template.content():
                references.append(template)
        print(f"{len(references)} templates to update:")
        for template in references:
            template.update_references(old_name, new_name)
            print(f"  {template.name()}")
        DocGenerator(self.tasklib).generate()
