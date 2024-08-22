from usys import stdin, stdout
from uselect import poll

def GetInput():
    stdout.flush()
    stdin.flush()
    return stdin.buffer.read(5)


