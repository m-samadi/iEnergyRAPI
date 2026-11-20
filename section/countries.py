from section import db_connect
from section import general
import requests
import json
import pandas

# Get all countries
def get_countries(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/countries"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the countries to a file
  with open("./output/countries.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the countries in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Country (\
  Code varchar(255), Description varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT Code FROM Country WHERE Code='" + str(df.loc[i, "Code"]) + "'")
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Country (Code, Description) \
      Values ('" + str(df.loc[i, "Code"]) + "', '" + str(df.loc[i, "Description"]) + "') ")

  # Display a message
  print("The countries part is done.")

# Get all regions
def get_regions(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/regions"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the regions to a file
  with open("./output/regions.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the regions in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Region (\
  Code varchar(255), Name varchar(255), CountryCode varchar(255), TimeZoneWindows varchar(255), TimeZoneIANA varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT Code FROM Region WHERE Code='" + str(df.loc[i, "Code"]) + "'")
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Region (Code, Name, CountryCode, TimeZoneWindows, TimeZoneIANA) \
      Values ('" + str(df.loc[i, "Code"]) + "', '" + str(df.loc[i, "Name"]) + "', '" + str(df.loc[i, "CountryCode"]) + "', '" +
      str(df.loc[i, "TimeZoneWindows"]) + "', '" + str(df.loc[i, "TimeZoneIANA"]) + "') ")

  # Display a message
  print("The regions part is done.")
