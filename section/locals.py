from section import db_connect
from section import general
import requests
import json
import pandas

# Find locals
def find_locals(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/locals"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the locals to a file
  with open("./output/locals.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the locals into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Local (\
  Id int PRIMARY KEY, Name varchar(255) NOT NULL, UserId int, ZipCodeId int, CountryCode varchar(255), LanguageCode varchar(255),\
  Region1 varchar(255), Region2 varchar(255), Region3 varchar(255), City varchar(255), Area2 varchar(255), Zip varchar(255),\
  Latitude float, Longitude float, IsStorage bit, CreatedDate varchar(255), CountryId varchar(255), Deleted bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Local WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      zip_code = df.loc[i, "ZipCode"]
      client.command("INSERT INTO Local (Id, Name, UserId, ZipCodeId, CountryCode, LanguageCode, Region1, Region2,\
      Region3, City, Area2, Zip, Latitude, Longitude, IsStorage, CreatedDate, CountryId, Deleted) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "UserId"])) + ", " +
      str(general.null_to_num(df.loc[i, "ZipCodeId"])) + ", '" + str(zip_code["CountryCode"]) + "', '" + str(zip_code["LanguageCode"]) + "', '" +
      str(zip_code["Region1"]) + "', '" + str(zip_code["Region2"]) + "', '" + str(zip_code["Region3"]) + "', '" + str(zip_code["City"]) + "', '" +
      str(zip_code["Area2"]) + "', '" + str(zip_code["Zip"]) + "', " + str(general.null_to_num(zip_code["Latitude"])) + ", " +
      str(general.null_to_num(zip_code["Longitude"])) + ", " + str(df.loc[i, "IsStorage"]) + ", '" + str(df.loc[i, "CreatedDate"]) + "', '" +
      str(df.loc[i, "CountryId"]) + "', " + str(df.loc[i, "Deleted"]) + ") ")

  # Display a message
  print("The locals part is done.")
