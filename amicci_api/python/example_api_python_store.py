#
# AUTHOR: Juliana Teixeira
# Requirements:
#   - Python 3.9.2 or later
# This PYTHON example send the data via post request to one of the APIs avaiable by Amicci. 
# It's a generic code, and simulates fictional number of data to be sent.
# The code iterates over a bunch of data and send a maximum number of data each time. The current maximum data
# per request is 20000.  
# The number of the requests to the API will depend on the ammount of data, because it has to respect
# the maximum data per request. 
# The data should be grouped and send the maximum possible at once.

import json
import requests
import time

MAX_DATA = 20000
MAX_QUANTITY = 10000
# URL of Amicci Store API
URL = ""
# Authorization token
TOKEN = ""

class Store:

    id_store = None
    name = None
    city = None
    state = None
    type = None
    date_launch = None
    zip_code = None
    format = None

    def __init__(self, id_store, name, city, state, type):
        if id_store is None:
            raise ValueError(f"Field id_store is mandatory")
        if name is None:
            raise ValueError(f"Field name is mandatory")
        if city is None:
            raise ValueError(f"Field city is mandatory")
        if state is None:
            raise ValueError(f"Field state is mandatory")
        if type is None:
            raise ValueError(f"Field type is mandatory")
        self.id_store = id_store
        self.name = name
        self.city = city
        self.state = state
        self.type = type

# Iterates over the maximum number of items to send
for i in range(1, MAX_DATA + 1, MAX_QUANTITY):
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in range(1, MAX_QUANTITY + 1):
        # Creates an object and adds in to the list
        try:
            # Creating Store type object with only mandatory fields
            store_obj = Store(j, f"Store_{j}", "São Paulo", "SP", "c")
            # Assigning non-mandatory values ​​to the Store object, if it exists
            store_obj.date_launch = "2024-01-01"
            store_obj.zip_code = "01415-002"
            store_obj.format = "c"
            list_json.append(store_obj.__dict__)
        except ValueError as e:
            print(f"Object {j} not constructed: {e}")
        except Exception as e:
            print(f"An error has occurred: {e}")

    # Converts the list to JSON format, which is required
    fields_string = json.dumps(list_json)

    # Initialize the request using the requests library
    try:
        headers = {"Content-Type": "application/json", "Authorization": TOKEN}
        response = None 
        print(f"Sending data to {URL}")
        response = requests.post(URL, data=fields_string, headers=headers, timeout=180)
        if response.status_code == 200 or response.status_code == 201:
            print(response.json())
            print(f"Data processed for data mass {j-MAX_QUANTITY}-{j} successfully")
        else:
            print(f"Data NOT processed for the data mass {j-MAX_QUANTITY}-{j}")                
        time.sleep(3)
    except Exception as e:
        print(f"Exception caught for data mass {j-MAX_QUANTITY}-{j}: {e}")