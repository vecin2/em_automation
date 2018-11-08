import os

def test_fs_example(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')

def test_fs_create_file_with_content(fs):
    fs.create_file('/var/data/xx1.txt',contents='hello')
    assert os.path.exists('/var/data/xx1.txt')
    with open('/var/data/xx1.txt') as f:
        assert "hello" == f.read()

def test_fs_create_same_file_does_not_through_duplicate_exc(fs):
    fs.create_file('/var/data/xx1.txt')
    assert os.path.exists('/var/data/xx1.txt')
