#***************************************************************
# main.py
#
# This tool retrieves real-time data from Cleanwatts Living Labs
# via the REST API.
#***************************************************************
from section import access
from section import sessions
import os
from section import units
from section import devices
from section import device_types
from section import tags
from section import data
from section import actuations
from section import algorithms
from section import assets
from section import benchmarks
from section import contracts
from section import countries
from section import documents

# Import the url and credentials
url = access.import_url()
login, password = access.import_credentials()

# Start a new session
token = sessions.create_session(url, login, password)

# Compose up the Docker container
curr_path = os.getcwd()
os.chdir("docker/dbengine")
os.system("docker compose up -d")
os.chdir(curr_path)

# Find information about units
units.find_units(url, token)

# Get information about devices
devices.get_devices(url, token)

# Get information about device types
device_types.get_device_types(url, token)

# Find information about tags
tags.find_tags(url, token)

# Get various data
data.get_data(url, token)
data.request_aggregated_data(url, token)
data.get_instant_data(url, token)

# Find information about actuations
actuations.find_actuations(url, token)

# Find information about algorithms
algorithms.find_algorithms(url, token)

# Get information about assets
assets.find_assets(url, token)
assets.Get_asset_types(url, token)

# Get information about benchmarks
benchmarks.get_benchmarks(url, token)
benchmarks.get_households(url, token)
benchmarks.get_habitation_areas(url, token)

# Get information about contracts
contracts.find_distribution_levels(url, token)
contracts.find_time_use_settings(url, token)
contracts.find_contracts(url, token)
contracts.find_contract_attributes(url, token)
contracts.find_contract_versions(url, token)
contracts.find_contract_codes(url, token)

# Get information about countries
countries.get_countries(url, token)
countries.get_regions(url, token)

# Get information about documents
documents.find_documents(url, token)
documents.find_document_fields(url, token)

# Compose down the Docker container
curr_path = os.getcwd()
os.chdir("docker/dbengine")
os.system("docker compose down")
os.chdir(curr_path)
