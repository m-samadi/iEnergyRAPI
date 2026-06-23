import json

# Import the url from the file
def import_url():
  with open("input/url.json") as file:
    json_data = json.load(file)
    url = json_data["URL"]
    file.close()

  return url

# Import the credentials from the file
def import_credentials():
  with open("input/credentials.json") as file:
    json_data = json.load(file)
    login = json_data["Login"]
    password = json_data["Password"]
    file.close()

  return login, password
