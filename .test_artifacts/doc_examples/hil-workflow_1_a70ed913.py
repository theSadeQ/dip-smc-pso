# Example from: docs\guides\workflows\hil-workflow.md
# Index: 1
# Runnable: True
# Hash: a70ed913

import struct
import zlib

# For command packet
payload = struct.pack("!I d", sequence_num, control_force)
crc = zlib.crc32(payload) & 0xFFFFFFFF
packet = payload + struct.pack("!I", crc)

# For state packet
payload = struct.pack("!I 6d", sequence_num, x, theta1, theta2, xdot, theta1dot, theta2dot)
crc = zlib.crc32(payload) & 0xFFFFFFFF
packet = payload + struct.pack("!I", crc)