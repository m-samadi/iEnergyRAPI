from section import db_connect
from section import general
import requests
import json
import pandas

# Find reports
def find_reports(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/reports"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the reports to a file
  with open("./output/reports.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the reports into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Report (\
  Id int PRIMARY KEY, Name varchar(255), Type int, Format int, ExportFormat int, Targets varchar(255),\
  NeedsInputs bit, TimeZoneIANA varchar(255), IsPublic bit, IsActive bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Report WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Report (Id, Name, Type, Format, ExportFormat, Targets, NeedsInputs, TimeZoneIANA, IsPublic, IsActive)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "Type"])) + ", " +
      str(general.null_to_num(df.loc[i, "Format"])) + ", " + str(general.null_to_num(df.loc[i, "ExportFormat"])) + ", '" + str(df.loc[i, "Targets"]) + "', " +
      str(df.loc[i, "NeedsInputs"]) + ", '" + str(df.loc[i, "TimeZoneIANA"]) + "', " + str(df.loc[i, "IsPublic"]) + ", " + str(df.loc[i, "IsActive"]) + ") ")

  # Display a message
  print("The reports part is done.")
