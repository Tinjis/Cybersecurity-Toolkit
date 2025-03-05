import paramiko
import getpass

def ssh_command(ip, port, user, password, cmd):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)

    stdin, stdout, stderr = client.exec_command(cmd)

    output = stdout.readlines() + stderr.readlines()

    if output:
        print("--> OutPut <---")
        for line in output:
            print(line.strip())

if __name__ == "__main__":
    user = input("Username: ")
    password = getpass.getpass()

    ip = input("Enter server IP: ")
    port = input("Enter port: ") 
    cmd = input("Enter command: ") 
    
    ssh_command(ip, port, user, password, cmd)
