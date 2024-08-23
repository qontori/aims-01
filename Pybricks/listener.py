from usys import stdin, stdout
from uselect import poll

def GetInput():
    print("rdy")
    #stdin is blocking so it must receieve 5 bytes inorder to run again
    return stdin.buffer.read(5)