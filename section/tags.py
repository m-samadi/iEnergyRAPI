from section import db_connect
from section import general
import requests
import json
import pandas

# Find tags
def find_tags(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/tags"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the tags to a file
  with open("./output/tags.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the tags in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Tag (\
  Id int, UnitId int, Name varchar(255), TagTypeId int, Virtual bit, CanActuate bit, DeviceId int, LocationId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Tag WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Tag (Id, UnitId, Name, TagTypeId, Virtual, CanActuate, DeviceId, LocationId)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", " + str(general.null_to_num(df.loc[i, "UnitId"])) + ", '" + str(df.loc[i, "Name"]) + "', " +
      str(general.null_to_num(df.loc[i, "TagTypeId"])) + ", " + str(df.loc[i, "Virtual"]) + ", " + str(df.loc[i, "CanActuate"]) + ", " +
      str(general.null_to_num(df.loc[i, "DeviceId"])) + ", " + str(general.null_to_num(df.loc[i, "LocationId"])) + ") ")

  # Display a message
  print("The tags part is done.")
