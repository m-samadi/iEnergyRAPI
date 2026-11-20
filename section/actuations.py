from section import db_connect
from section import general
import requests
import json
import pandas

# Find actuations
def find_actuations(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/actuations"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the actuations to a file
  with open("./output/actuations.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the actuations in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Actuation (\
  Id int, Command varchar(255), Action int, Acknowledged bit, OccurrenceDate varchar(255), TagId int, Status int, LastOccurrenceDate varchar(255), LastResponse varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  client.command("TRUNCATE TABLE Actuation")
  for i in range(len(df)):
    client.command("INSERT INTO Actuation (Id, Command, Action, Acknowledged, OccurrenceDate, TagId, Status, LastOccurrenceDate, LastResponse)\
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Command"]) + "', " + str(general.null_to_num(df.loc[i, "Action"])) + ", " +
    str(df.loc[i, "Acknowledged"]) + ", '" + str(df.loc[i, "OccurrenceDate"]) + "', " + str(general.null_to_num(df.loc[i, "TagId"])) + ", " +
    str(general.null_to_num(df.loc[i, "Status"])) + ", '" + str(df.loc[i, "LastOccurrenceDate"]) + "', '" + str(df.loc[i, "LastResponse"]) + "') ")

  # Display a message
  print("The actuations part is done.")
