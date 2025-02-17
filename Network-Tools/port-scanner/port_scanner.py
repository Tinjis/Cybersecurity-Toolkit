import socket

def ports_scanning(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  

    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"The Port {port} is Open.")
    sock.close()  

def scan_target(ip, start_port, end_port):
    print(f"Scanning The Target IP: {ip}...")
    for port in range(start_port, end_port + 1):
        ports_scanning(ip, port)

if __name__ == "__main__":
    target_ip = input("Enter The Target IP: ")  
    start_port = int(input("Enter The Start Port: "))  
    end_port = int(input("Enter The End Port: "))  

    scan_target(target_ip, start_port, end_port)