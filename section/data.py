from section import db_connect
from section import general
import json
import requests
from datetime import date
import pandas

# Get data
def get_data(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Import the configuration from the file
  with open("input/data.json") as file:
    json_data = json.load(file)
    granularity = json_data["Granularity"]
    from_date = json_data["From"]
    file.close()

  # Set the manual configuration
  to_date = date.today().isoformat()

  # Insert the data into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Data (\
  Consumption float, Date varchar(255), Read float, ConsumptionCost float, Cost float, TagId int, ValueType int, CostMeasurementUnitId float\
  ) ENGINE MergeTree")

  df = None
  result_tag = client.query("SELECT Id FROM Tag")
  for i in range(len(result_tag.result_rows)):
    # Determine the API endpoint to communicate with
    request_url = url + "/api/2.0/data/" + granularity + "?tags=" + str(result_tag.result_rows[i][0]) + "&from=" + from_date + "&to=" + to_date

    # Perform a GET request to the API
    response = requests.get(request_url, headers=headers)
    
    # Get the response in JSON format
    response_json = response.json()

    # Display the response
    #print(response_json)

    # Write the data to a file
    with open("./output/data/data_" + str(result_tag.result_rows[i][0]) + ".json", "w") as file:
      json.dump(response_json, file)
      file.close()

    df = pandas.concat([df, pandas.DataFrame.from_dict(response_json)], axis=0, ignore_index=True)

  raws = []
  for j in range(len(df)):
    raw = []
    raw.append(general.null_to_num(df.loc[j, "Consumption"]))
    raw.append(df.loc[j, "Date"])
    raw.append(general.null_to_num(df.loc[j, "Read"]))
    raw.append(general.null_to_num(df.loc[j, "ConsumptionCost"]))
    raw.append(general.null_to_num(df.loc[j, "Cost"]))
    raw.append(general.null_to_num(df.loc[j, "TagId"]))
    raw.append(general.null_to_num(df.loc[j, "ValueType"]))
    raw.append(general.null_to_num(df.loc[j, "CostMeasurementUnitId"]))

    raws.append(raw)

  client.insert("Data", raws, column_names=["Consumption", "Date", "Read", "ConsumptionCost", "Cost", "TagId", "ValueType", "CostMeasurementUnitId"])

  # Display a message
  print("The data part is done.")

# Request aggregated data
def request_aggregated_data(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Import the configuration from the file
  with open("input/data.json") as file:
    json_data = json.load(file)
    granularity = json_data["Granularity"]
    from_date = json_data["From"]
    file.close()

  # Set the manual configuration
  to_date = date.today().isoformat()

  # Insert the aggregated data into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS AggregatedData (\
  TagId int, Date varchar(255), Value float, ValueCurrency float, CurrencySymbol varchar(255), ValueType int\
  ) ENGINE MergeTree")

  df = None
  result_tag = client.query("SELECT Id FROM Tag")
  for i in range(len(result_tag.result_rows)):
    # Determine the API endpoint to communicate with
    request_url = url + "/api/2.0/data/request/" + granularity + "?tags=" + str(result_tag.result_rows[i][0]) + "&from=" + from_date + "&to=" + to_date

    # Perform a GET request to the API
    response = requests.get(request_url, headers=headers)
    
    # Get the response in JSON format
    response_json = response.json()

    # Display the response
    #print(response_json)

    # Write the aggregated data to a file
    with open("./output/data/aggregated_data_" + str(result_tag.result_rows[i][0]) + ".json", "w") as file:
      json.dump(response_json, file)
      file.close()

    df = pandas.concat([df, pandas.DataFrame.from_dict(response_json)], axis=0, ignore_index=True)

  raws = []
  for j in range(len(df)):
    raw = []
    raw.append(general.null_to_num(df.loc[j, "TagId"]))
    raw.append(df.loc[j, "Date"])
    raw.append(general.null_to_num(df.loc[j, "Value"]))
    raw.append(general.null_to_num(df.loc[j, "ValueCurrency"]))
    raw.append(str(df.loc[j, "CurrencySymbol"]))
    raw.append(general.null_to_num(df.loc[j, "ValueType"]))

    raws.append(raw)

  client.insert("AggregatedData", raws, column_names=["TagId", "Date", "Value", "ValueCurrency", "CurrencySymbol", "ValueType"])

  # Display a message
  print("The aggregated data part is done.")

# Get instant data
def get_instant_data(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Import the configuration from the file
  with open("input/data.json") as file:
    json_data = json.load(file)
    granularity = json_data["Granularity"]
    from_date = json_data["From"]
    file.close()

  # Set the manual configuration
  to_date = date.today().isoformat()

  # Insert the instant data into the database
  client = db_connect.connect()

  client.command("CREATE TABLE IF NOT EXISTS InstantData (\
  UnitId int, Granularity varchar(255), TagId int, Date varchar(255), Average float, Minimum float, Maximum float, Last float, Count int, ValueType int\
  ) ENGINE MergeTree")

  df = None
  result_tag = client.query("SELECT Id FROM Tag")
  for i in range(len(result_tag.result_rows)):
    # Determine the API endpoint to communicate with
    request_url = url + "/api/2.0/instants/" + granularity + "?tags=" + str(result_tag.result_rows[i][0]) + "&from=" + from_date + "&to=" + to_date

    # Perform a GET request to the API
    response = requests.get(request_url, headers=headers)
    
    # Get the response in JSON format
    response_json = response.json()

    # Display the response
    #print(response_json)

    # Write the instant data to a file
    with open("./output/data/instant_data_" + str(result_tag.result_rows[i][0]) + ".json", "w") as file:
      json.dump(response_json, file)
      file.close()

    df = pandas.concat([df, pandas.DataFrame.from_dict(response_json)], axis=0, ignore_index=True)

  raws = []
  for j in range(len(df)):
    raw = []
    raw.append(general.null_to_num(df.loc[j, "UnitId"]))
    raw.append(df.loc[j, "Granularity"])
    raw.append(general.null_to_num(df.loc[j, "TagId"]))
    raw.append(df.loc[j, "Date"])
    raw.append(general.null_to_num(df.loc[j, "Average"]))
    raw.append(general.null_to_num(df.loc[j, "Minimum"]))
    raw.append(general.null_to_num(df.loc[j, "Maximum"]))
    raw.append(general.null_to_num(df.loc[j, "Last"]))
    raw.append(general.null_to_num(df.loc[j, "Count"]))
    raw.append(general.null_to_num(df.loc[j, "ValueType"]))

    raws.append(raw)

  client.insert("InstantData", raws, column_names=["UnitId", "Granularity", "TagId", "Date", "Average", "Minimum", "Maximum", "Last", "Count", "ValueType"])

  # Display a message
  print("The instant data part is done.")
