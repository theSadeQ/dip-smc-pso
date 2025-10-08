# Example from: docs\hil_quickstart.md
# Index: 1
# Runnable: True
# Hash: 08325789

import struct
import zlib

# For control packet: sequence + command
payload = struct.pack("!I d", sequence_num, control_force)
crc = zlib.crc32(payload) & 0xFFFFFFFF
packet = payload + struct.pack("!I", crc)

# For state packet: sequence + 6 measurements
payload = struct.pack("!I 6d", sequence_num, x, theta1, theta2, x_dot, theta1_dot, theta2_dot)
crc = zlib.crc32(payload) & 0xFFFFFFFF
packet = payload + struct.pack("!I", crc)