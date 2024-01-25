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
# URL of Amicci Product API
URL = ""
# Authorization token
TOKEN = ""

class Product:

    id_product = None
    name = None
    n1 = None
    n2 = None
    n3 = None
    n4 = None
    n5 = None
    n6 = None
    n7 = None
    n8 = None
    ean = None
    private_label_flag = None
    id_seller = None
    brand = None
    unity = None
    date_launch = None

    def __init__(self, id_product, name, n1, n2, n3, brand):
        if id_product is None:
            raise ValueError(f"Field id_product is mandatory")
        if name is None:
            raise ValueError(f"Field name is required")
        if n1 is None:
            raise ValueError(f"Field n1 is mandatory")
        if n2 is None:
            raise ValueError(f"Field n2 is mandatory")
        if n3 is None:
            raise ValueError(f"Field n3 is mandatory")
        if brand is None:
            raise ValueError(f"Field brand is mandatory")
        self.id_product = id_product
        self.name = name
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.brand = brand

# Iterates over the maximum number of items to send
for i in range(1, MAX_DATA + 1, MAX_QUANTITY):
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in range(1, MAX_QUANTITY + 1):
        # Creates an object and adds it to the list
        try:
            # Creating Product type object with only mandatory fields
            product_obj = Product(f"product_{j}", f"name_{j}", "unity", "Bebida", "Cerveja", f"brand{j}")
            # Assigning non-mandatory values ​​to the Product type object, if it exists
            product_obj.n4 = ""
            product_obj.n5 = ""
            product_obj.n6 = ""
            product_obj.n7 = ""
            product_obj.n8 = ""
            product_obj.ean = "7894900019902"
            product_obj.private_label_flag = "1"
            product_obj.id_seller = f"seller_{j}"
            product_obj.unity = "l"
            product_obj.date_launch = "2024-01-01"
            list_json.append(product_obj.__dict__)
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