import sys
import socket
import threading

translation_mapping = {}
for i in range(256):
    ch = chr(i)
    if len(repr(ch)) == 3:
        translation_mapping[i] = ch
    else:
        translation_mapping[i] = "."
TRANSLATION_TABLE = translation_mapping

def hex_dump(data, length=16, display=True):
    if isinstance(data, bytes):
        data = data.decode(errors='ignore')
    
    result = []
    for i in range(0, len(data), length):
        segment = data[i:i+length]
        readable = segment.translate(TRANSLATION_TABLE)
        
        hex_values_list = []
        for char in segment:
            hex_values_list.append(f"{ord(char):02X}")
        hex_values = ' '.join(hex_values_list)
        
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
    
    try:
        if receive_first:
            remote_data = receive_data(remote_socket)
            if remote_data:
                print(f"[<-] Received {len(remote_data)} bytes from remote")
                hex_dump(remote_data)
                client_socket.send(remote_data)
        
        while True:
            
            local_data = receive_data(client_socket)
            remote_data = receive_data(remote_socket)
            
            
            if local_data:
                print(f"[->] Received {len(local_data)} bytes from client")
                hex_dump(local_data)
                remote_socket.send(modify_request(local_data))
                
            if remote_data:
                print(f"[<-] Received {len(remote_data)} bytes from remote")
                hex_dump(remote_data)
                client_socket.send(modify_response(remote_data))
            
            
            if not local_data and not remote_data:
                break
                
    finally:
        client_socket.close()
        remote_socket.close()
        print("[*] Connections closed")

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
        print("Usage: ./tcp_inspector.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./tcp_inspector.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() == "true"
    
    start_server(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == "__main__":
    main()

