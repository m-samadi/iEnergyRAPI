from section import db_connect
from section import general
import requests
import json
import pandas

# Find distribution levels
def find_distribution_levels(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/distributionlevels"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the distribution levels to a file
  with open("./output/distribution_levels.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the distribution levels in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS DistributionLevel (\
  Id int, Name varchar(255), Country varchar(255), UtilityTypeId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM DistributionLevel WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO DistributionLevel (Id, Name, Country, UtilityTypeId) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', '" +
      str(df.loc[i, "Country"]) + "', " + str(general.null_to_num(df.loc[i, "UtilityTypeId"])) + ") ")

  # Display a message
  print("The distribution levels part is done.")

# Find time use settings
def find_time_use_settings(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/timeuse/settings"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the time use settings to a file
  with open("./output/time_use_settings.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the time use settings in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS TimeUseSetting (\
  Id int, Name varchar(255), SeasonSeriesId int, HolidayAsSunday bit, Official bit, Dummy bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM TimeUseSetting WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO TimeUseSetting (Id, Name, SeasonSeriesId, HolidayAsSunday, Official, Dummy) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "SeasonSeriesId"])) + ", " +
      str(df.loc[i, "HolidayAsSunday"]) + ", " + str(df.loc[i, "Official"]) + ", " + str(df.loc[i, "Dummy"]) + ") ")

  # Display a message
  print("The time use settings part is done.")

# Find contracts
def find_contracts(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/contracts"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the contracts to a file
  with open("./output/contracts.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the contracts in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Contract (\
  Id int, Code varchar(255), ContractTypeId int, RegionCode varchar(255), GroupIds int, SupplierId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Contract WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Contract (Id, Code, ContractTypeId, RegionCode, GroupIds, SupplierId) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Code"]) + "', " + str(general.null_to_num(df.loc[i, "ContractTypeId"])) + ", '" +
      str(df.loc[i, "RegionCode"]) + "', " + str(general.null_to_num(df.loc[i, "GroupIds"][0])) + ", " + str(general.null_to_num(df.loc[i, "SupplierId"])) + ") ")

  # Display a message
  print("The contracts part is done.")

# Find contract attributes
def find_contract_attributes(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/contract/attributes"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the contract attributes to a file
  with open("./output/contract_attributes.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the contract attributes in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS ContractAttribute (\
  Id int, Name varchar(255), Type int, ValueType int, MeasurementUnit int, MinValue varchar(255), MaxValue varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM ContractAttribute WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO ContractAttribute (Id, Name, Type, ValueType, MeasurementUnit, MinValue, MaxValue) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "Type"])) + ", " +
      str(general.null_to_num(df.loc[i, "ValueType"])) + ", " + str(general.null_to_num(df.loc[i, "MeasurementUnit"])) + ", '" + str(df.loc[i, "MinValue"]) + "', '" +
      str(df.loc[i, "MaxValue"]) + "') ")

  # Display a message
  print("The contract attributes part is done.")

# Find contract versions
def find_contract_versions(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/contract/versions"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the contract versions to a file
  with open("./output/contract_versions.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the contract versions in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS ContractVersion (\
  Id int, ContractId int, StartDate varchar(255), Version int, DistributionLevelId int, DistributionLevelCycleId int, TimeUseSettingId int, DocumentTypeId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM ContractVersion WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO ContractVersion (Id, ContractId, StartDate, Version, DistributionLevelId, DistributionLevelCycleId, TimeUseSettingId, DocumentTypeId) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", " + str(general.null_to_num(df.loc[i, "ContractId"])) + ", '" + str(df.loc[i, "StartDate"]) + "', " +
      str(general.null_to_num(df.loc[i, "Version"])) + ", " + str(general.null_to_num(df.loc[i, "DistributionLevelId"])) + ", " + str(general.null_to_num(df.loc[i, "DistributionLevelCycleId"])) + ", " +
      str(general.null_to_num(df.loc[i, "TimeUseSettingId"])) + ", " + str(general.null_to_num(df.loc[i, "DocumentTypeId"])) + ") ")

  # Display a message
  print("The contract versions part is done.")

# Find contract codes
def find_contract_codes(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/contracts/codes"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the contract codes to a file
  with open("./output/contract_codes.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the contract codes in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS ContractCode (\
  GroupId int, ContractCode varchar(255), ContractTypeId int, RegionCode varchar(255), ContractIds int, SupplierId int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  client.command("TRUNCATE TABLE ContractCode")
  for i in range(len(df)):
    client.command("INSERT INTO ContractCode (GroupId, ContractCode, ContractTypeId, RegionCode, ContractIds, SupplierId) \
    Values (" + str(general.null_to_num(df.loc[i, "GroupId"])) + ", '" + str(df.loc[i, "ContractCode"]) + "', " + str(general.null_to_num(df.loc[i, "ContractTypeId"])) + ", '" +
    str(df.loc[i, "RegionCode"]) + "', " + str(general.null_to_num(df.loc[i, "ContractIds"][0])) + ", " + str(general.null_to_num(df.loc[i, "SupplierId"])) + ") ")

  # Display a message
  print("The contract codes part is done.")
