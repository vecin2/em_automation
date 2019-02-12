import sys
from io import StringIO
from prompt_toolkit import prompt
from unittest.mock import patch
#with patch('prompt_toolkit.prompt', return_value="dddd"):
#    print(prompt("hi"))
@patch('prompt_toolkit.prompt',return_value="jjjj")
def somethin(prompt):
    print(prompt("hi"))

somethin()

#f = open('somefile.txt')
#sys.stdin =f
##sys.stdin =StringIO("hola\nadios\nholawithPrompt\n")
#
#print(input("say something"))
##print(input("say something"))
#print(input("say bye"))
#prompt("this is prompt ")
