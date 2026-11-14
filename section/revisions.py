from section import db_connect
from section import general
import requests
import json
import pandas

# Return defined revision sources
def return_revision_sources(url, token): 
  # Set the headers for the request
  headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/revisions/sources"

  # Perform a GET request to the API
  response = requests.get(request_url, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Write the revision sources to a file
  with open("./output/revision_sources.json", "w") as file:
    json.dump(response_json, file)
    file.close()

  # Insert information of the revision sources into the database
  client = db_connect.connect()
  client.command("CREATE TABLE IF NOT EXISTS RevisionSource (\
  SourceId int PRIMARY KEY, Name varchar(255), Priority int, IsEstimated bit, IsTemporary bit\
  ) ENGINE MergeTree")

  df = pandas.DataFrame.from_dict(response_json)

  for i in range(len(df)):
    result = client.query("SELECT SourceId FROM RevisionSource WHERE SourceId=" + str(df.loc[i, "SourceId"]))
    if len(result.result_rows) == 0:
      client.command("INSERT INTO RevisionSource (SourceId, Name, Priority, IsEstimated, IsTemporary) \
      Values (" + str(general.null_to_num(df.loc[i, "SourceId"])) + ", '" + str(df.loc[i, "Name"]) + "', " + str(general.null_to_num(df.loc[i, "Priority"])) + ", " +
      str(df.loc[i, "IsEstimated"]) + ", " + str(df.loc[i, "IsTemporary"]) + ") ")

  # Display a message
  print("The revision sources part is done.")
