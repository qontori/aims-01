from usys import stdin, stdout
from uselect import poll

def GetInput():
    print("rdy")
    stdout.flush()
    #stdin is blocking so it must receieve 5 bytes inorder to run again
    data = stdin.buffer.read(5)
    return data