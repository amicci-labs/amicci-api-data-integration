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
# URL of Amicci Sellout API
URL = ""
# Authorization token
TOKEN = ""

class Sellout:

    date = None
    id_product = None
    id_store = None
    quantity = None
    sale_gross = None
    sale_liquid = None
    cost_gross = None
    cost_liquid = None
    sale_channel = None

    def __init__(self, date, id_product, id_store, quantity, sale_gross, sale_liquid):
        if date is None:
            raise ValueError(f"Field Date is mandatory")
        if id_product is None:
            raise ValueError(f"Field id_product is mandatory")
        if id_store is None:
            raise ValueError(f"Field id_store is mandatory")
        if quantity is None:
            raise ValueError(f"Field quantity is mandatory")
        if sale_gross is None:
            raise ValueError(f"Field sale_gross is mandatory")
        if sale_liquid is None:
            raise ValueError(f"Field sale_liquid is mandatory")
        self.date = date
        self.id_product = id_product
        self.id_store = id_store
        self.quantity = quantity
        self.sale_gross = sale_gross
        self.sale_liquid = sale_liquid

# Iterates over the maximum number of items to send
for i in range(1, MAX_DATA + 1, MAX_QUANTITY):
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in range(1, MAX_QUANTITY + 1):
        # Creates an object and adds it to the list
        try:
            # Creating Sellout type object with only mandatory fields
            sellout_obj = Sellout("2024-01-01", f"product_{j}", f"store_{j}", "15", "30", "20")
            # Assigning non-mandatory values ​​to the Sellout type object, if it exists
            sellout_obj.cost_gross = "25"
            sellout_obj.cost_liquid = "15"
            sellout_obj.sale_channel = "online"
            list_json.append(sellout_obj.__dict__)
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
            print(f"Data NOT processed for data mass {j-MAX_QUANTITY}-{j}")                
        time.sleep(3)
    except Exception as e:
        print(f"Exception caught for data mass {j-MAX_QUANTITY}-{j}: {e}")