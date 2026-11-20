from section import db_connect
from section import general
import requests
import json
import pandas

# Find units
def find_units(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/units"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the units to a file
  with open("./output/units.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the units in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Unit (\
  Id int PRIMARY KEY, Name varchar(255) NOT NULL, StateId int, MacAddress varchar(255), TimeZoneId varchar(255),\
  TimeZoneIANA varchar(255), HashedSerial varchar(255), Interval int, LastComm varchar(255), TypeId int,\
  ProtocolId int, Deleted bit, IsActive bit, IsConnected bit, DataCollectionStatus int, Reference varchar(255),\
  CommThreshold int, ProductionYear int, Serial varchar(255), HasComments bit, HasDevices bit, LocalId int,\
  MonthlyObjective float, LastConfigDate varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Unit WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Unit (Id, Name, StateId, MacAddress, TimeZoneId, TimeZoneIANA, HashedSerial, Interval, LastComm,\
      TypeId, ProtocolId, Deleted, IsActive, IsConnected, DataCollectionStatus, Reference, CommThreshold,\
      ProductionYear, Serial, HasComments, HasDevices, LocalId, MonthlyObjective, LastConfigDate) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "StateId"])) + ", '" +
      str(df.loc[i, "MacAddress"]) + "', '" + str(df.loc[i, "TimeZoneId"]) + "', '" + str(df.loc[i, "TimeZoneIANA"]) + "', '" +
      str(df.loc[i, "HashedSerial"]) + "', " + str(general.null_to_num(df.loc[i, "Interval"])) + ", '" + str(df.loc[i, "LastComm"]) + "', " +
      str(general.null_to_num(df.loc[i, "TypeId"])) + ", " + str(general.null_to_num(df.loc[i, "ProtocolId"])) + ", " + str(df.loc[i, "Deleted"]) + ", " +
      str(df.loc[i, "IsActive"]) + ", " + str(df.loc[i, "IsConnected"]) + ", " + str(general.null_to_num(df.loc[i, "DataCollectionStatus"])) + ", '" +
      str(df.loc[i, "Reference"]) + "', " + str(general.null_to_num(df.loc[i, "CommThreshold"])) + ", " + str(general.null_to_num(df.loc[i, "ProductionYear"])) + ", '" +
      str(df.loc[i, "Serial"]) + "', " + str(df.loc[i, "HasComments"]) + ", " + str(df.loc[i, "HasDevices"]) + ", " +
      str(general.null_to_num(df.loc[i, "LocalId"])) + ", " + str(general.null_to_num(df.loc[i, "MonthlyObjective"])) + ", '" + str(df.loc[i, "LastConfigDate"]) + "') ")

  # Display a message
  print("The units part is done.")
