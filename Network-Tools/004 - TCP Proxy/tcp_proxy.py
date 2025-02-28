import sys
import socket
import threading

HEX_TABLE = ""
for i in range(256):
    character = chr(i)
    if len(repr(character)) == 3:
        HEX_TABLE += character
    else:
        HEX_TABLE += "."

TRANSLATION_TABLE = str.maketrans(HEX_TABLE, HEX_TABLE)

def hex_dump(data, length=16, display=True):
    if isinstance(data, bytes):
        data = data.decode(errors='replace')
    
    result = []
    for i in range(0, len(data), length): 
        segment = data[i:i+length]
        readable = segment.translate(TRANSLATION_TABLE)

        hex_values = []
        for char in segment:
            hex_values.append(f"{ord(char):02X}")
        hex_values = ' '.join(hex_values)

        formatted_output = f"{i:04x} {hex_values:<{length * 3}} {readable}"
        result.append(formatted_output)
    
    if display:
        for line in result:
            print(line)
    else:
        return result

def receive_data(connection):
    buffer = b""
    connection.settimeout(5)
    
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    
    return buffer

def modify_request(buffer):
    return buffer

def modify_response(buffer):
    return buffer

def handle_proxy(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    if receive_first:
        remote_data = receive_data(remote_socket)
        hex_dump(remote_data)
        remote_data = modify_response(remote_data)
        if remote_data:
            print(f"[->] Sending {len(remote_data)} bytes to localhost.")
            client_socket.send(remote_data)
    
    while True:
        local_data = receive_data(client_socket)
        if local_data:
            print(f"[->] Received {len(local_data)} bytes from localhost.")
            hex_dump(local_data)
            local_data = modify_request(local_data)
            remote_socket.send(local_data)
            print("[->] Sent to remote.")
        
        remote_data = receive_data(remote_socket)
        if remote_data:
            print(f"[->] Received {len(remote_data)} bytes from remote.")
            hex_dump(remote_data)
            remote_data = modify_response(remote_data)
            client_socket.send(remote_data)
            print("[->] Sent to localhost.")
        
        if not local_data or not remote_data:
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break

def start_server(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((local_host, local_port))
    except Exception as error:
        print(f"[!] Binding error: {error}\n[X] Failed to bind on {local_host}:{local_port}")
        sys.exit(0)
    
    print(f"[*] Listening on {local_host}:{local_port}")
    server.listen(5)
    
    while True:
        client_socket, client_address = server.accept()
        print(f"[->] Incoming connection from {client_address[0]}:{client_address[1]}")
        
        proxy_thread = threading.Thread(target=handle_proxy, args=(
            client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() == "true"
    
    start_server(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == "__main__":
    main()

