"""
@object: Implementation of a serial server to retrieve and back up data
         and metadata from a prototype as part of a dual-screen smartphone 
         experience.
@author: PECCHIOLI Mathieu
"""
# IMPORT LIBRAIRIES
from serial import Serial
from Package.package_serial import decode, readMetadata
from os import system

# SETTING UP SERIAL PORTS
ast1 = Serial()
ast2 = Serial()
ast1.baudrate = 9600
ast2.baudrate = 9600
ast1.port = '/dev/ttyACM0'
ast2.port = '/dev/ttyACM1'

# OPEN SERIAL PORTS
ast1.open()
ast2.open()

# RUNNING
system('clear')
print("SERVER STARTED\n\n")
while True:
    # READ SERIAL PORT 1
    while ast1.in_waiting:
        data = ast1.read(1).decode('utf-8')
        if data == '$':
            frame = ast1.read(7).decode('utf-8')
            decode(1, frame)

    # READ SERIAL PORT 2
    while ast2.in_waiting:
        data = ast2.read(1).decode('utf-8')
        if data == '$':
            frame = ast2.read(7).decode('utf-8')
            decode(1, frame)
    
    # CLEAR SCREENS
    with open("./Data/commands.txt", 'r') as f:
        clear = f.read()

    if clear == '1':
        ast1.write(b'0')
        ast2.write(b'0')
        with open("./Data/commands.txt", 'w') as f:
            f.write('0')

# CLOSE SERIAL PORTS
ast1.close()
ast2.close()