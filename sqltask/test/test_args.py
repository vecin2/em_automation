from argparse import ArgumentParser

parser = ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)

parser2 = ArgumentParser()

def test_some():
    input_str = "blabla -t -p"
    parser2.add_argument("-t",action='store_true')
    args = parser2.parse_args(["-t"])
    """ assert "blabla" ==vars(args) """
    assert True == args.t
