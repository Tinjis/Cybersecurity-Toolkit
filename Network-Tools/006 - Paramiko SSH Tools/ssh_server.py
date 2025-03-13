import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))

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
    ssh_port = 2222

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

