from section import db_connect
from section import general
import json
from datetime import date
import requests
import pandas

# Find documents
def find_documents(url, token): 
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

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/documents" + "?fromDate=" + from_date + "&toDate=" + to_date

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the documents to a file
  with open("./output/documents.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the documents in the database
  '''
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS Document (\
  \
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM Document WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("")
  '''
  # Display a message
  print("The documents part is done.")

# Find document fields
def find_document_fields(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/documentfields"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the document fields to a file
  with open("./output/document_fields.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert or update information of the document fields in the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS DocumentField (\
  Id int, Code varchar(255), Description varchar(255), IsNumeric bit, IsAccumulated bit, MeasurementUnit int\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json["List"])

  for i in range(len(df)):
    result = client.query("SELECT Id FROM DocumentField WHERE Id=" + str(df.loc[i, "Id"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO DocumentField (Id, Code, Description, IsNumeric, IsAccumulated, MeasurementUnit)\
      Values (" + str(general.null_to_num(df.loc[i, "Id"])) + ", '" + str(df.loc[i, "Code"]) + "', '" + str(df.loc[i, "Description"]) + "', " +
      str(df.loc[i, "IsNumeric"]) + ", " + str(df.loc[i, "IsAccumulated"]) + ", " + str(general.null_to_num(df.loc[i, "MeasurementUnit"])) + ") ")

  # Display a message
  print("The document fields part is done.")
