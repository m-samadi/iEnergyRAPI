from section import db_connect
from section import general
import requests
import json
import pandas

# Find suppliers
def find_suppliers(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/suppliers"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the suppliers to a file
  with open("./output/suppliers.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the suppliers into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Supplier (\
  Id int PRIMARY KEY, Name varchar(255), MeasurementType int, MeasurementUnit int, Deleted bit, CountryCode varchar(255), UtilityTypeId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Supplier WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Supplier (Id, Name, MeasurementType, MeasurementUnit, Deleted, CountryCode, UtilityTypeId)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "MeasurementType"])) + ", " +
      str(general.null_to_num(df.loc[i, "MeasurementUnit"])) + ", " + str(df.loc[i, "Deleted"]) + ", '" + str(df.loc[i, "CountryCode"]) + "', " +
      str(general.null_to_num(df.loc[i, "UtilityTypeId"])) + ") ")

  # Display a message
  print("The suppliers part is done.")
