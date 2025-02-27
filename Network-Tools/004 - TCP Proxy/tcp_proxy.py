import sys
import socket
import threading


HEX_FILTER = ""

for i in range(256):
    char = chr(i)

    if len(repr(char)) == 3:
        HEX_FILTER += char

    else:
        HEX_FILTER += "."

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i : i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])

        hexwidth = length * 3
        
        results.append(f"{i:04x} {hexa:<{hexwidth}} {printable}")

    if show:
        for line in results:
            print(line)
    else:
        return results
    

def receive_from(connection):
    buffer = b""
    connection.settimeout(5)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    
    except Exception as e:
        pass

    return buffer


def request_handler(buffer):
    
    return buffer

def response_handler(buffer):

    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_host.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)

    if len(remote_buffer):
        print(f"[->] Sending {len(remote_buffer)} to localhost")
        client_socket.send(remote_buffer)

    while True:

        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print(f"[->]Received {local_buffer} bytes from localhost.")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[->] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[->] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            
            print("[*] No more data. Closing connections.")
            break

