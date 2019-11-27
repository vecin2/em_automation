import pathlib
from shutil import copyfile
import os
import sys
import io

import lxml.etree as ET

#parser = ET.XMLParser(strip_cdata=False)
#tree =ET.parse(filepath,parser)
def is_process(process_path):
    parser = ET.XMLParser(encoding="utf-8")
    text = process_path.read_text()
    str_text = text.encode("utf-8")
    import pdb;pdb.set_trace() 
    tree = ET.fromstring(str_text).getroottree()
    assert "dd" == type(tree)
    doctype ==tree.docinfo.doctype
    print("doctype is: "+doctype)
    return "ProcessDefinition" == doctype
    #return "PackageEntry" in str(process_path.read_text())

def extend_process(process_path,target=None):
    if not process_path.exists():
        print("No process found under '"+str(process_path)+"'")
    elif is_process(process_path):
        print("Extending process under '"+str(process_path)+"'")
        os.makedirs(str(target), exist_ok=True)
        copyfile(process_path, target/os.path.basename(process_path))
    else:
        print("Not a valid xml process found under '"+str(process_path)+"'")

def main():
    src = pathlib.Path(sys.argv[1])
    if sys.argv[2]:
        dst = pathlib.Path(sys.argv[2])
    extend_process(src,dst)

# Run it only if called from the command line
if __name__ == '__main__':
        main()
