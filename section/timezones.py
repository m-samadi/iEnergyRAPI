from section import db_connect
from section import general
import requests
import json
import pandas

# Find timezones
def find_timezones(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/timezones"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the timezones to a file
  with open("./output/timezones.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the timezones into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Timezone (\
  Id varchar(255) PRIMARY KEY, DisplayName varchar(255), Offset int) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Timezone WHERE Id='" + df.loc[i, "Id"] + "'")
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Timezone (Id, DisplayName, Offset) \
      Values ('" + str(df.loc[i, "Id"]) + "', '" + str(df.loc[i, "DisplayName"]) + "', " +
      str(general.null_to_num(df.loc[i, "Offset"])) + ") ")

  # Display a message
  print("The timezones part is done.")
