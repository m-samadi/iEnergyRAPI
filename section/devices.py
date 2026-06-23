from section import db_connect
from section import general
import requests
import json
import pandas

# Get devices
def get_devices(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/devices"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the devices to a file
  with open("./output/devices.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the devices in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Device (\
  Id int, Serial varchar(255), Name varchar(255), DeviceTypeId int, UnitId int, Interval int, IsCommunicating bit,\
  DataCollectionStatus int, Index_ int, Address varchar(255), State int, Reference varchar(255), Deleted bit,\
  Virtual bit, PhysicalAddress varchar(255), PhysicalAddressType varchar(255), HasTags bit, HasNotes bit, TariffId int,\
  ContractedOptionId int, LocalId int, DeviceTypeTypeCode varchar(255), Domain varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Device WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Device (Id, Serial, Name, DeviceTypeId, UnitId, Interval, IsCommunicating, DataCollectionStatus,\
      Index_, Address, State, Reference, Deleted, Virtual, PhysicalAddress, PhysicalAddressType, HasTags, HasNotes, TariffId,\
      ContractedOptionId, LocalId, DeviceTypeTypeCode, Domain) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Serial"]) + "', '" + str(df.loc[i, "Name"]) + "', " +
      str(general.null_to_num(df.loc[i, "DeviceTypeId"])) + ", " + str(general.null_to_num(df.loc[i, "UnitId"])) + ", " + str(general.null_to_num(df.loc[i, "Interval"])) + ", " +
      str(df.loc[i, "IsCommunicating"]) + ", " + str(general.null_to_num(df.loc[i, "DataCollectionStatus"])) + ", " + str(general.null_to_num(df.loc[i, "Index"])) + ", '" +
      str(df.loc[i, "Address"]) + "', " + str(general.null_to_num(df.loc[i, "State"])) + ", '" + str(df.loc[i, "Reference"]) + "', " +
      str(df.loc[i, "Deleted"]) + ", " + str(df.loc[i, "Virtual"]) + ", '" + str(df.loc[i, "PhysicalAddress"]) + "', '" +
      str(df.loc[i, "PhysicalAddressType"]) + "', " + str(df.loc[i, "HasTags"]) + ", " + str(df.loc[i, "HasNotes"]) + ", " +
      str(general.null_to_num(df.loc[i, "TariffId"])) + ", " + str(general.null_to_num(df.loc[i, "ContractedOptionId"])) + ", " + str(general.null_to_num(df.loc[i, "LocalId"])) + ", '" +
      str(df.loc[i, "DeviceTypeTypeCode"]) + "', '" + str(df.loc[i, "Domain"]) + "') ")

  # Display a message
  print("The devices part is done.")
