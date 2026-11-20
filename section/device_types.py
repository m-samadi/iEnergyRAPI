from section import db_connect
from section import general
import requests
import json
import pandas

# Get device types
def get_device_types(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/deviceTypes"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the device types to a file
  with open("./output/device_types.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the device types in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS DeviceType (\
  Id int, Name varchar(255), MeasurementTypeId int, Series int, Type varchar(255), Class varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM DeviceType WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO DeviceType (Id, Name, MeasurementTypeId, Series, Type, Class) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "MeasurementTypeId"])) + ", " +
      str(general.null_to_num(df.loc[i, "Series"])) + ", '" + str(df.loc[i, "Type"]) + "', '" + str(df.loc[i, "Class"]) + "') ")

  # Display a message
  print("The device types part is done.")
