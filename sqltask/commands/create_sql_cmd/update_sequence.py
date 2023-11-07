from datetime import datetime

from sqltask.emproject.emsvn import EMSvn


class UpdateSequenceWriter(object):
    FAILED_SEQ_NO = -1

    def __init__(self, sequence_generator):
        self.seq_generator = sequence_generator
        self.update_seq_no = None
        self.excinfo = None

    def write(self, parent_folder):
        self._compute_update_seq_no()
        update_sequence = f"PROJECT $Revision: {self.update_seq_no} $"
        (parent_folder / "update.sequence").write_text(update_sequence)

    def on_finish(self):
        if self.failed_computing_seq_no():
            self.display_unable_to_compute_seq_no()
        else:
            self.display_update_seq_no_computed(self.update_seq_no)

    def failed_computing_seq_no(self):
        return self.excinfo is not None

    def _compute_update_seq_no(self):
        try:
            self.update_seq_no = self.seq_generator.generate_seq_no()
        except Exception as excinfo:
            self.update_seq_no = UpdateSequenceWriter.FAILED_SEQ_NO
            self.excinfo = excinfo
        return self.update_seq_no

    def display_unable_to_compute_seq_no(self):
        message = f"Defaulting to 'PROJECT $Revision:  {self.update_seq_no}  $'. \nMake sure you update it manually!!"
        print("Unable to compute sequece no:")
        print(str(self.excinfo))
        print(message)

    def display_update_seq_no_computed(self, number):
        print("update.sequence is '" + str(number) + "'")

    def displaying_computing_rev_no(self, sequence_generator_name):
        print(f"Computing 'update.sequence' from {sequence_generator_name}")


class SVNRevNoGenerator(object):
    def __init__(self, project_root, offset):
        self.emsvn = EMSvn(project_root)
        self.offset = offset

    def name(self):
        return "SVN revision number"

    def generate_seq_no(self):
        try:
            rev_no = self.emsvn.revision_number()
            revision_no = int(rev_no)
            revision_no = revision_no + 1 + int(self.offset)
            # displayer.update_seq_no_computed(revision_no)
        except Exception as excinfo:
            revision_no = -1
            # displayer.unable_to_compute_seq_no("-1", excinfo)
        return revision_no


class TimeStampGenerator(object):
    def generate_seq_no(self):
        return int(datetime.timestamp(datetime.now()))

    def name(self):
        return "Timestamp"
