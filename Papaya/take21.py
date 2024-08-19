#for hub
#for gpt
from pybricks.hubs import PrimeHub
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

hub = PrimeHub()

# Set up Bluetooth communication
client = BluetoothMailboxClient()
mailbox = TextMailbox('signal', client)

# Replace with the MAC address of your Raspberry Pi's Bluetooth adapter
raspberry_pi_address = 'hciconfig'
client.connect(raspberry_pi_address)

# Send a signal to the Raspberry Pi to start detection
mailbox.send('START')

# Wait for the result
direction = mailbox.wait()

# Handle the result
if direction == "Left":
    hub.display.text("L")
elif direction == "Right":
    hub.display.text("R")

# Send a stop signal (optional)
mailbox.send('STOP')
