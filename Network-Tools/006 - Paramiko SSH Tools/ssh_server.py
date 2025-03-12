import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))

HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, "test_rsa.key"))

class Server (paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == "username") and (password == "password"):
            return paramiko.AUTH_SUCCESSFUL
        

if __name__ == "__main__":
    server = "192.168.1.9"
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)

        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print(f"[X] Listen failed: {str(e)}")
        sys.exit(1)
    else:
        print(f"[+] Got a connection! {client}, {addr}")            
    
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(HOSTKEY)
    server = Server()
    bhsession.start_server(server=server)
    chan = bhsession.accept(20)
    if chan is None:
        print("[X] No Channel.")
        sys.exit(1)

    