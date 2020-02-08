import pathlib
import os
import shutil

def Path(path):
    return pathlib.Path(path)

tempfolder =Path(os.path.dirname(__file__))/ ".tempfolder"

def clear_tempfolder():
    if tempfolder.exists():
        shutil.rmtree(tempfolder)
    #os.rmdir(tempfolder)

clear_tempfolder()
