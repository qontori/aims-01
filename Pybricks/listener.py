from usys import stdin, stdout
from uselect import poll

def GetInput():
    stdout.flush()
    print("rdy")
    return stdin.buffer.read(5)


