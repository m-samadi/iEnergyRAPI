from section import db_connect
from section import general
import requests
import json
import pandas

# Get all possible member values
def get_member_values(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/integration/memberOptions"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the member values to a file
  with open("./output/member_values.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert member values into the database
  client = db_connect.connect()

  client.command("CREATE TABLE IF NOT EXISTS RECMemberSector (Id int, Name varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["RECMemberSectors"])
  client.command("TRUNCATE TABLE RECMemberSector")
  for i in range(len(df)):
    client.command("INSERT INTO RECMemberSector (Id, Name)\
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  client.command("CREATE TABLE IF NOT EXISTS RECMemberType (Id int, Name varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["RECMemberTypes"])
  client.command("TRUNCATE TABLE RECMemberType")
  for i in range(len(df)):
    client.command("INSERT INTO RECMemberType (Id, Name)\
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  client.command("CREATE TABLE IF NOT EXISTS RECMemberState (Id int, Name varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["RECMemberStates"])
  client.command("TRUNCATE TABLE RECMemberState")
  for i in range(len(df)):
    client.command("INSERT INTO RECMemberState (Id, Name)\
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  # Display a message
  print("The member values part is done.")

# Get all possible retail contract values
def get_retail_contract_values(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/integration/retailContractOptions"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the retail contract values to a file
  with open("./output/retail_contract_values.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert retail contract values into the database
  client = db_connect.connect()

  client.command("CREATE TABLE IF NOT EXISTS ContractType (Id int PRIMARY KEY, Name varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["ContractTypes"])
  for i in range(len(df)):
    result = client.query("SELECT Id FROM ContractType WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO ContractType (Id, Name)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  client.command("CREATE TABLE IF NOT EXISTS DocumentType (Id int PRIMARY KEY, Name varchar(255)) ENGINE MergeTree")
  for entry in response_json["TariffTypes"]:
    if entry["DocumentTypes"]:
      df = pandas.DataFrame.from_dict(entry["DocumentTypes"])
      for i in range(len(df)):
        result = client.query("SELECT Id FROM DocumentType WHERE Id=" + str(df.loc[i, "Id"]))
        if len(result.result_rows) == 0:
          client.command("INSERT INTO DocumentType (Id, Name)\
          Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  # Display a message
  print("The retail contract values part is done.")

# Get all possible REC contract values
def get_REC_contract_values(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/integration/recContractOptions"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the REC contract values to a file
  with open("./output/REC_contract_values.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert REC contract values into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS RECReportFrequence (Id int, Name varchar(255)) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["RECReportFrequences"])

  client.command("TRUNCATE TABLE RECReportFrequence")
  for i in range(len(df)):
    client.command("INSERT INTO RECReportFrequence (Id, Name)\
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]) + "') ")

  # Display a message
  print("The REC contract values part is done.")
