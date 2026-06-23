import requests

# Create a new session
def create_session(url, login, password):
  # Set the authentication data
  auth_data = {
    "Login": login,
    "Password": password
  }

  # Set the headers for the request
  headers = {
    "Content-Type": "application/json",
  }

  # Determine the API endpoint to communicate with
  request_url = url + "/api/2.0/sessions"

  # Perform a POST request to the API
  response = requests.post(request_url, json=auth_data, headers=headers)
  
  # Get the response in JSON format
  response_json = response.json()

  # Display the response
  #print(response_json)

  # Get the token from the response
  token = response_json["Token"]

  # Display the status code
  #print(response.status_code)

  # Display a message
  print("A new session is created.")

  return token
