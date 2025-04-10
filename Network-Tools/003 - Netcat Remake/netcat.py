import socket
import threading
import sys
import shlex
import subprocess
import textwrap
import argparse

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.output.decode()}"


class NetCat:
    
    def __init__(self, arguments, buffer=None):

        self.arguments = arguments
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):

        if self.arguments.listen:
            self.listen()
        else:
            self.send()

    def send(self):

        self.socket.connect((self.arguments.target, self.arguments.port))

        if self.buffer:
            self.socket.send(self.buffer)

        try:

            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                
                if response:

                    print(response)
                    buffer = input('> ')
                    buffer += '\n'

                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:

            print("User terminated.")
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.arguments.target, self.arguments.port))

        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):

        if self.arguments.execute:
            output = execute(self.arguments.execute)
            client_socket.send(output.encode())
        
        elif self.arguments.upload:
            file_buffer = b""
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.arguments.upload, "wb") as f:
                f.write(file_buffer)
                message = f"Saved file {self.arguments.upload}"
                client_socket.send(message.encode())
            
        elif self.arguments.command:
            cmd_buffer = b""

            while True:
                try:

                    client_socket.send(b"-> ")

                    while "\n" not in cmd_buffer.decode():

                        cmd_buffer += client_socket.recv(64)

                    response = execute(cmd_buffer.decode())

                    if response:
                        client_socket.send(response.encode())
                        cmd_buffer = b""
                    
                except Exception as e:
                    print(f"Server error: {e}")
                    client_socket.close()  
                    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remake of the netcat tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
Example:
netcat.py -t 192.168.1.108 -p 5555 -l -c          # command shell
netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt  # upload to file
netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"  # execute command
echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135      # echo text to server port 135
netcat.py -t 192.168.1.108 -p 5555                   # connect to server
'''))
    
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='target port (default: 5555)')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='IP to bind/listen (default: 0.0.0.0)')
    parser.add_argument('-u', '--upload', help='upload file')
    
    arguments = parser.parse_args()
    
    if arguments.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    
    nc = NetCat(arguments, buffer.encode())
    nc.run()
