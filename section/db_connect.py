import json
import clickhouse_connect

# Connect to the ClickHouse database
def connect():
  with open("input/db.json") as file:
    json_data = json.load(file)
    host_val = json_data["Host"]
    username_val = json_data["Username"]
    password_val = json_data["Password"]
    file.close()

  return clickhouse_connect.get_client(host=host_val, username=username_val, password=password_val)
