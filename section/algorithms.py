from section import db_connect
from section import general
import requests
import json
import pandas

# Find algorithms
def find_algorithms(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/algorithms"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the algorithms to a file
  with open("./output/algorithms.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the algorithms in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Algorithm (\
  Id int, Name varchar(255), Internal bit, Guid varchar(255), DefaultPriority int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Algorithm WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Algorithm (Id, Name, Internal, Guid, DefaultPriority) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(df.loc[i, "Internal"]) + ", '" +
      str(df.loc[i, "Guid"]) + "', " + str(general.null_to_num(df.loc[i, "DefaultPriority"])) + ") ")

  # Display a message
  print("The algorithms part is done.")
