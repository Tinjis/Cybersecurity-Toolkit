import paramiko

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
    pass