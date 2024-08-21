from usys import stdin, stdout
from uselect import poll

test = "tes"
def GetInput():
    global test
    stdout.flush()
    print("rdy")
    test = stdin.buffer.read(5)


