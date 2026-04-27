import socket
import time
import json
import random
import numpy as np

IP = '192.168.0.103'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Starting DIPPID sender on UDP port", PORT)

while True:
    current_time = time.time()
    
    # Simulate accelerometer using numpy sine and cosine functions
    acc_x = float(np.sin(current_time * 2.0))
    acc_y = float(np.cos(current_time * 1.5))
    acc_z = float(np.sin(current_time * 0.5))
    
    # Simulate button press randomly (10% chance)
    btn_1 = 1 if random.random() < 0.1 else 0
    
    # Format matches DIPPID
    data = {
        "accelerometer": {
            "x": acc_x,
            "y": acc_y,
            "z": acc_z
        },
        "button_1": btn_1
    }
    
    message = json.dumps(data)
    print("Sending:", message)
    
    sock.sendto(message.encode(), (IP, PORT))
    
    # Sleep to simulate around 50Hz update rate
    time.sleep(0.02)
