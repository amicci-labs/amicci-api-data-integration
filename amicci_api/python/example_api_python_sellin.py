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
# URL of Amicci Sellin API
URL = ""
# Authorization token
TOKEN = ""

class Sellin:
    
    date = None
    id_invoice = None
    purchase_value_gross = None
    purchase_value_liquid = None
    quantity = None
    id_product = None
    id_seller = None
    
    def __init__(self, date, id_invoice, purchase_value_gross, purchase_value_liquid, quantity, id_product):
        if date is None:
            raise ValueError(f"Field date is mandatory")
        if id_invoice is None:
            raise ValueError(f"Field id_invoice is mandatory")
        if purchase_value_gross is None:
            raise ValueError(f"Field purchase_value_gross is mandatory")
        if purchase_value_liquid is None:
            raise ValueError(f"Field purchase_value_liquid is mandatory")
        if quantity is None:
            raise ValueError(f"Field quantity is mandatory")
        if id_product is None:
            raise ValueError(f"Field id_product is mandatory")
        self.date = date
        self.id_invoice = id_invoice
        self.purchase_value_gross = purchase_value_gross
        self.purchase_value_liquid = purchase_value_liquid
        self.quantity = quantity
        self.id_product = id_product

# Iterates over the maximum number of items to send
for i in range(1, MAX_DATA + 1, MAX_QUANTITY):
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in range(1, MAX_QUANTITY + 1):
        # Creates an object and adds it to the list
        try:
            # Creating Sellin type object with only mandatory fields
            sellin_obj = Sellin("2024-01-01", f"invoice{j}", "30", "15", "10", f"product{j}")
            # Assigning non-mandatory values ​​to the Sellin object, if it exists
            sellin_obj.id_seller = f"seller_{j}"
            list_json.append(sellin_obj.__dict__)
        except ValueError as e:
            print(f"Object {j} not constructed: {e}")
        except Exception as e:
            print(f"An error has occurred: {e}")

    # Convert list to JSON format, which is required
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