from section import db_connect
from section import general
import requests
import json
import pandas

# Get measurement units
def get_measurement_units(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/measurementUnits"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the measurement units to a file
  with open("./output/measurement_units.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the measurement units into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS MeasurementUnit (\
  Id int PRIMARY KEY, Name varchar(255), SmallName varchar(255), IsCurrency bit) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT Id FROM MeasurementUnit WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO MeasurementUnit (Id, Name, SmallName, IsCurrency) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]).replace("'", "''") + "', '" +
      str(df.loc[i, "SmallName"]) + "', " + str(df.loc[i, "IsCurrency"]) + ") ")

  # Display a message
  print("The measurement units part is done.")
