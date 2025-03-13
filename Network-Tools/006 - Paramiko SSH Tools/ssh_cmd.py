import paramiko
import getpass

def interactive_ssh(ip, port, user, password):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=int(port), username=user, password=password)
    
    print(f"Connected to {ip}:{port}. Enter commands, or type 'exit' to quit.")
    
    try:
        while True:
            cmd = input("Enter command (or 'exit' to quit): ")
            if cmd.lower() == 'exit':
                break
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read() + stderr.read()
            if output:
                print("--> Output <---")
                print(output.decode())
            else:
                print("--> No output received. <--")
    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    user = input("Username: ")
    password = getpass.getpass()
    ip = input("Enter server IP: ")
    port = input("Enter port: ")
    
    interactive_ssh(ip, port, user, password)


