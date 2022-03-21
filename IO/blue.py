#import glob
import os
import random
import subprocess
import time

from bluetooth import *

# Enable the pi's bluetooth interface for scanning
p = subprocess.check_output(['sudo', 'hciconfig', 'hci0', 'piscan'])

# Set up the socket
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

# Advertise a service
port = server_sock.getsockname()[1]
uuid='94f39d29-7d6d-437d-973b-fba39e49d4ee'
advertise_service(server_sock, 'Test server',
        service_id = uuid,
        service_classes = [uuid, SERIAL_PORT_CLASS],
        profiles = [SERIAL_PORT_PROFILE],
        protocols = [OBEX_UUID]
        )

# Acquire connection
print(f'Waiting for connection from RFCOMM channel {port}')
client_sock, client_info = server_sock.accept()
print(f'Accepted connection from {client_info}')

def recv_and_format(socket):
    recvd = socket.recv(1024).decode()
    recvd = recvd.replace('\n', '')
    recvd = recvd.replace('\r', '')
    return recvd

# Receive data
while True:
    try:
        cmd = recv_and_format(client_sock)

        print(f'Received {cmd}')

        data = None
        # Open temperature file from mirror code and send info back to client
        if cmd == 'temp':
            with open('../inweather.csv', 'r') as wf:
                temp = wf.readlines()
            data = temp[0]

        # Open tasks file and add an entry
        elif cmd.startswith('taskadd '):
            task = cmd[len('taskadd '):]
            print(f'Adding task {task}')
            with open('../tasks.txt', 'a') as wf:
                wf.write(f'{task}\n')

        # Open calendar file and add a calendar
        elif cmd.startswith('caladd '):
            event = cmd[len('caladd '):]
            print(f'Adding calendar event {event}')
            with open('../calendar.txt', 'a') as wf:
                wf.write(f'{event}\n')

        # Change the user's name displayed in the UI
        elif cmd.startswith('username '):
            username = cmd[len('username '):]
            print(f'Set username to {username}')
            with open('../username.txt', 'w') as wf:
                wf.write(username)

        else:
            pass

        if data:
            print(f'Sending {data}')
            client_sock.send(data)

    except IOError:
        pass

    except KeyboardInterrupt:
        print('Disconnected')
        client_sock.close()
        exit()
