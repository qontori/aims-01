#receiving input back to primehub

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Icon
from pybricks.tools import wait
import link2

lines = link2.strip()
# Initialize the hub
hub = PrimeHub()

# Read the command from the text file
#command = read_and_return_file_contents('/home/robothink/Desktop/raspi2prime/input.txt')

# Perform actions based on the command read from the file
def lineRead():
    if lines == 'left':
        hub.display.char("K")  
    elif lines == 'right':
        hub.display.char("R")  
    elif lines == 'forward':
        hub.display.char("F")  
    elif lines == 'backward':
        hub.display.char("B") 
    else:
        hub.display.icon(Icon.SAD) 

if __name__ == "__main__":
    lineRead()
    wait(5000)
