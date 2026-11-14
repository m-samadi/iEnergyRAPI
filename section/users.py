from section import db_connect
from section import general
import requests
import json
import pandas

# Find users
def find_users(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/users"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the users to a file
  with open("./output/users.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the users into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS User (\
  Id int PRIMARY KEY, Key varchar(255), Login varchar(255), Application int, Email varchar(255), Name varchar(255), Language varchar(255),\
  Profile int, Currency int, Created varchar(255), Deleted bit, Blocked bit, Configured bit, Providers varchar(255),\
  Newsletter bit, Units varchar(255), CurrencySymbol varchar(255), Active bit, ReceiveSmsNotifications bit,\
  ReceiveEmailNotifications bit, SingleSession bit, TwoFactor bit, IsLdapUser bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM User WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO User (Id, Key, Login, Application, Email, Name, Language, Profile,\
      Currency, Created, Deleted, Blocked, Configured, Providers, Newsletter, Units, CurrencySymbol,\
      Active, ReceiveSmsNotifications, ReceiveEmailNotifications, SingleSession, TwoFactor, IsLdapUser)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Key"]) + "', '" + str(df.loc[i, "Login"]) + "', " +
      str(general.null_to_num(df.loc[i, "Application"])) + ", '" + str(df.loc[i, "Email"]) + "', '" + str(df.loc[i, "Name"]) + "', '" +
      str(df.loc[i, "Language"]) + "', " + str(general.null_to_num(df.loc[i, "Profile"])) + ", " + str(general.null_to_num(df.loc[i, "Currency"])) + ", '" +
      str(df.loc[i, "Created"]) + "', " + str(df.loc[i, "Deleted"]) + ", " + str(df.loc[i, "Blocked"]) + ", " + str(df.loc[i, "Configured"]) + ", '" +
      str(df.loc[i, "Providers"]) + "', " + str(df.loc[i, "Newsletter"]) + ", '" + str(df.loc[i, "Units"]) + "', '" + str(df.loc[i, "CurrencySymbol"]) + "', " +
      str(df.loc[i, "Active"]) + ", " + str(df.loc[i, "ReceiveSmsNotifications"]) + ", " + str(df.loc[i, "ReceiveEmailNotifications"]) + ", " +
      str(df.loc[i, "SingleSession"]) + ", " + str(df.loc[i, "TwoFactor"]) + ", " + str(df.loc[i, "IsLdapUser"]) + ") ")

  # Display a message
  print("The users part is done.")

# Return information for users forms data
def return_user_form_data(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/user-form-data"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the users forms data to a file
  with open("./output/user_form_data.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the users forms data into the database
  client = db_connect.connect()

  client.command("CREATE TABLE IF NOT EXISTS ProfileType (ProfileTypeId int PRIMARY KEY, Name varchar(255), Level int) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["ProfileTypes"])
  for i in range(len(df)):
    result = client.query("SELECT ProfileTypeId FROM ProfileType WHERE ProfileTypeId=" + str(df.loc[i, "ProfileTypeId"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO ProfileType (ProfileTypeId, Name, Level) \
      Values (" + str(general.null_to_num(df.loc[i, "ProfileTypeId"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "Level"])) + ") ")

  client.command("CREATE TABLE IF NOT EXISTS Language (LanguageId int PRIMARY KEY, Name varchar(255), Code varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["Languages"])
  for i in range(len(df)):
    result = client.query("SELECT LanguageId FROM Language WHERE LanguageId=" + str(df.loc[i, "LanguageId"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Language (LanguageId, Name, Code) \
      Values (" + str(general.null_to_num(df.loc[i, "LanguageId"])) + ", '" + str(df.loc[i, "Name"]) + "', '" + str(df.loc[i, "Code"]) + "') ")

  client.command("CREATE TABLE IF NOT EXISTS Currency (Id int PRIMARY KEY, Name varchar(255), SmallName varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["Currencies"])
  for i in range(len(df)):
    result = client.query("SELECT Id FROM Currency WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Currency (Id, Name, SmallName) \
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Name"]).replace("'", "''") + "', '" + str(df.loc[i, "SmallName"]) + "') ")

  client.command("CREATE TABLE IF NOT EXISTS ApplicationType (Id int PRIMARY KEY, Application varchar(255), Name varchar(255)) ENGINE MergeTree")
  client.command("CREATE TABLE IF NOT EXISTS Instance (Id int PRIMARY KEY, ApplicationTypeId int, Key varchar(255), Name varchar(255)) ENGINE MergeTree")
  df = pandas.DataFrame.from_dict(response_json["ApplicationTypes"])
  client.command("TRUNCATE TABLE ApplicationType")
  client.command("TRUNCATE TABLE Instance")
  for i in range(len(df)):
    client.command("INSERT INTO ApplicationType (Id, Application, Name) \
    Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Application"]) + "', '" + str(df.loc[i, "Name"]) + "') ")
    for item in df.loc[i, "Instances"]:
      client.command("INSERT INTO Instance (Id, ApplicationTypeId, Key, Name) \
      Values (" + str(general.null_to_num(item["Id"])) + ", " + str(general.null_to_num(df.loc[i, "Id"])) + ", '"
      + str(item["Key"]) + "', '" + str(item["Name"]) + "') ")

  # Display a message
  print("The users forms data part is done.")
