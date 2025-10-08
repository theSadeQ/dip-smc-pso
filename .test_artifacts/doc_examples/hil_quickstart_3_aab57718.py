# Example from: docs\hil_quickstart.md
# Index: 3
# Runnable: True
# Hash: aab57718

import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 9001))

while True:
    data, addr = sock.recvfrom(1024)
    # Unpack state: timestamp, x, θ1, θ2, ẋ, θ̇1, θ̇2
    state = struct.unpack('!7f', data)

    # Your controller logic here
    control_force = your_controller(state[1:])  # Exclude timestamp

    # Send control response
    response = struct.pack('!2f', state[0], control_force)
    sock.sendto(response, addr)