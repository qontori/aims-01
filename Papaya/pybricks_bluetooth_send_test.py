import bricksrl_hub
import numpy as np
import struct

state_dim = 7
action_dim = 4
action_format_str = "!" + "f" * action_dim
action = np.zeros(action_dim)
byte_action = struct.pack(action_format_str, *action)
hub = bricksrl_hub.PybricksHub( out_format_str = "!" + "f" * state_dim, state_dim= state_dim)

hub.connect()
while True:
    hub.send(byte_action)