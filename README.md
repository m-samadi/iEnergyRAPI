# The iEnergyRAPI Tool
iEnergyRAPI is a tool for obtaining real-time data from Cleanwatts Living Labs via REST API. This process is related to renewable energy communities and can be used in various applications, such as digital twins and AI agents.

## Requirements
The following dependencies must be met before running the tool:
* Python (>=3.10)
* Docker (docker compose)
* venv or conda

If docker-compose does not exist on your system, it can be installed as follows:
```
sudo apt install docker-compose
```
The requests module is used to connect to the labs via API, which can be installed with pip as shown below:
```
python -m pip install requests
```
The Pandas package is applied for data manipulation and can be installed using the following command:
```
pip install pandas
```
To connect ClickHouse to Python, you need to install the ClickHouse Connect driver, which can be done via pip, as mentioned below:
```
pip install clickhouse-connect
```

## Virtual Environment
The sandbox environment can be created and activated as shown below to keep the overall system clean:
```
python3 -m venv env  # create
source env/bin/activate  # activate
```

Note that this environment should be activated before each use. It can be deactivated using the following command:
```
deactivate
```

## ClickHouse Database
The ClickHouse database is provided via a docker container in the "docker/dbengine" folder. It can be installed and started automatically when running the tool. However, these processes can also be performed using the commands below:
```
cd docker/dbengine
docker compose up -d
```
You can use your optional information (e.g., credentials) in the docker-compose.yml file before using the above commands or before the first execution of the tool. The connection information is available in the db.josn file in the "input" folder, which is used by the tool to connect to the database. The database is available at http://localhost:8123/. It can also be manually terminated as follows:
```
docker compose down
```

## Run the Tool
To connect to Living Labs, you need to provide the URL and credentials. This information is available in the url.json and credentials.json files in the "input" folder. However, the credentials have been removed, and only authorized users can use their privileges granted by Cleanwatts Digital. Furthermore, the granularity and date range can be defined in the data.json file, also located in the same folder. This information is necessary for some functions, such as requesting aggregated data. The tool can be run using the following command:
```
python3 main.py
```

Each piece of the obtained data is stored in JSON format in the "output" folder and in the ClickHouse database. It is possible to connect to the database via the local URL mentioned above and view the data using SQL queries. However, some data is also available in the "result" folder. The "database" folder contains a backup of the database based on the data obtained.

## Modeling
The class diagram is created using the Modelio modeling tool, based on the data obtained. The "modeling" folder contains the Modelio project and the diagram.

## TODO
New sections will be added to obtain more information from Living Labs.
