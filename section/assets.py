from section import db_connect
from section import general
import requests
import json
import pandas

# Find assets
def find_assets(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/assets"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the assets to a file
  with open("./output/assets.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the assets in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Asset (\
  Id int, Name varchar(255), TypeId int, Active bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Asset WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Asset (Id, Name, TypeId, Active) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " +
      str(general.null_to_num(df.loc[i, "TypeId"])) + ", " + str(df.loc[i, "Active"]) + ") ")

  # Display a message
  print("The assets part is done.")

# Get asset types
def Get_asset_types(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/assets/types"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the asset types to a file
  with open("./output/asset_types.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the asset types in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS AssetType (\
  Id int, Name varchar(255), IsFlexible bit, DomainId int, Domain varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM AssetType WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO AssetType (Id, Name, IsFlexible, DomainId, Domain) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(df.loc[i, "IsFlexible"]) + ", " +
      str(general.null_to_num(df.loc[i, "DomainId"])) + ", '" + str(df.loc[i, "Domain"]) + "') ")

  # Display a message
  print("The asset types part is done.")
