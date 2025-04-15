#!/usr/bin/env python3

import os
import paramiko
import socket
import sys
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

CWD = os.path.dirname(os.path.realpath(__file__))
KEY_PATH = os.path.join(CWD, "test_rsa.key")

if not os.path.exists(KEY_PATH):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    with open(KEY_PATH, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
HOSTKEY = paramiko.RSAKey(filename=KEY_PATH)

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == "username" and password == "password":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

if __name__ == "__main__":
    server_ip = "0.0.0.0" 
     
    while True:
        try:
            ssh_port = int(input("Enter port to listen on (default 2222): ") or 2222)
            if 1 <= ssh_port <= 65535:
                break
            else:
                print("Invalid port. Please enter a value between 1 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a numeric port.")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_ip, ssh_port))
        sock.listen(100)

        print("[+] Listening for incoming SSH connections...")
        client, addr = sock.accept()
    except Exception as e:
        print(f"[X] Failed to listen: {str(e)}")
        sys.exit(1)
    else:
        print(f"[+] Connection received from {addr}")

    ssh_session = paramiko.Transport(client)
    ssh_session.add_server_key(HOSTKEY)
    server = SSHServer()

    try:
        ssh_session.start_server(server=server)
        channel = ssh_session.accept(20)
        if channel is None:
            print("[X] No valid channel received.")
            sys.exit(1)

        print("[+] Client authenticated.")
        print(channel.recv(1024).decode())
        channel.send("Welcome.")

        while True:
            try:
                command = input("Enter command: ")
                if command.lower() == "exit":
                    channel.send("exit")
                    print("Exiting SSH session...")
                    ssh_session.close()
                    break
                
                channel.send(command)
                response = channel.recv(8192)
                print(response.decode())

            except Exception as e:
                print(f"[X] Error sending command: {str(e)}")
                break

    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
        ssh_session.close()

