from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait

# Replace 'your_device_address' with the address of your LEGO Spike Prime Hub
HUB_ADDRESS = '10:17:84:55:EE:55'

# Initialize the hub
hub = PrimeHub()

motor = Motor(Port.A)

# Example function to send a command
def send_command(command):
    # You might need to adapt this depending on your specific commands and hub setup
    if command == 'forward':
        motor.run_time(500, 1000)  # Adjust parameters as needed
    elif command == 'backward':
        motor.run_time(-500, 1000)  # Adjust parameters as needed
    else:
        print("Unknown command")

# Example usage
send_command('forward')
wait(1000)
send_command('backward')