from section import db_connect
from section import general
import requests
import json
import pandas

# Get benchmarks
def get_benchmarks(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/residentialbenchmark"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the benchmarks to a file
  with open("./output/benchmarks.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the benchmarks in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Benchmark (\
  CountryCode varchar(255), HouseholdId int, Household varchar(255), HabitationAreaId int, HabitationArea varchar(255),\
  AverageAnualConsumption float, AverageMonthlyConsumption float, AverageWeeklyConsumption float, AverageDailyConsumption float\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  client.command("TRUNCATE TABLE Benchmark")
  for i in range(len(df)):
    client.command("INSERT INTO Benchmark (CountryCode, HouseholdId, Household, HabitationAreaId, HabitationArea,\
    AverageAnualConsumption, AverageMonthlyConsumption, AverageWeeklyConsumption, AverageDailyConsumption) \
    Values ('" + str(df.loc[i, "CountryCode"]) + "', " + str(general.null_to_num(df.loc[i, "HouseholdId"])) + ", '" + str(df.loc[i, "Household"]) + "', " +
    str(general.null_to_num(df.loc[i, "HabitationAreaId"])) + ", '" + str(df.loc[i, "HabitationArea"]) + "', " + str(general.null_to_num(df.loc[i, "AverageAnualConsumption"])) + ", " +
    str(general.null_to_num(df.loc[i, "AverageMonthlyConsumption"])) + ", " + str(general.null_to_num(df.loc[i, "AverageWeeklyConsumption"])) + ", " + str(general.null_to_num(df.loc[i, "AverageDailyConsumption"])) + ") ")

  # Display a message
  print("The benchmarks part is done.")

# Get households
def get_households(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/households"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the households to a file
  with open("./output/households.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the households in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Household (\
  HouseholdId int, HouseholdName varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT HouseholdId FROM Household WHERE HouseholdId=" + str(df.loc[i, "HouseholdId"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO Household (HouseholdId, HouseholdName) \
      Values (" + str(general.null_to_num(df.loc[i, "HouseholdId"])) + ", '" + str(df.loc[i, "HouseholdName"]) + "') ")

  # Display a message
  print("The households part is done.")

# Get habitation areas
def get_habitation_areas(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/habitationAreas"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the habitation areas to a file
  with open("./output/habitation_areas.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the habitation areas in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS HabitationArea (\
  HabitationAreaId int, HabitationAreaName varchar(255)\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT HabitationAreaId FROM HabitationArea WHERE HabitationAreaId=" + str(df.loc[i, "HabitationAreaId"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO HabitationArea (HabitationAreaId, HabitationAreaName) \
      Values (" + str(general.null_to_num(df.loc[i, "HabitationAreaId"])) + ", '" + str(df.loc[i, "HabitationAreaName"]) + "') ")

  # Display a message
  print("The habitation areas part is done.")
