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

# Total number of itens, in that case it should come from a file/database etc. But in out example it will be a fixed number.
MAX_DATA = 40000
# Max itens per post request in the API
MAX_QUANTITY = 20000

# URL of the Product API (follow Amicci official links for the API URL)
URL = ""
# Authorization Token (provided by Amicci official webiste, available at https://platform.amicci.com.br/home)
TOKEN = ""

#Verify if URL and TOKEN were provided
if URL is None or TOKEN is None:
    print("Must provide a valid URL and a valid TOKEN")
    exit()

# Class object with the available fields
class Product:

    #Required
    id_product = None
    brand = None
    name = None
    n1 = None
    n2 = None
    n3 = None

    #Optional
    n4 = None
    n5 = None
    n6 = None
    n7 = None
    n8 = None
    ean = None
    private_label_flag = None
    id_seller = None
    unity = None
    date_launch = None

    def __init__(self, id_product, name, n1, n2, n3, brand):
        if id_product is None:
            raise ValueError(f"Field id_product is required")
        if name is None:
            raise ValueError(f"Field name is required")
        if n1 is None:
            raise ValueError(f"Field n1 is required")
        if n2 is None:
            raise ValueError(f"Field n2 is required")
        if n3 is None:
            raise ValueError(f"Field n3 is required")
        if brand is None:
            raise ValueError(f"Field brand is required")
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
            # Creating object with required fields
            obj = Product(j+i-1, f"product_name_{j+i-1}", "unity", "Bebida", "Cerveja", f"product_brand_{j+i-1}")
            # Assign optional fields if available
            obj.n4 = "n4"
            obj.n5 = "n5"
            obj.n6 = "n6"
            obj.n7 = "n7"
            obj.n8 = "n8"
            obj.ean = "7894900019902"
            obj.private_label_flag = "1"
            obj.id_seller = j+i-1
            obj.unity = "l"
            obj.date_launch = "2020-05-05"
            list_json.append(obj.__dict__)
        except Exception as e:
            print(f"Object {j+i-1} not constructed: {e}")

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
            print(f"Data processed from {i} to {i + MAX_QUANTITY-1} successfully")
        else:
            print(f"Data NOT processed from {i} to {i + MAX_QUANTITY-1} successfully")              
        time.sleep(3)
    except Exception as e:
        print(f"Exception caught for on data {i} to {i + MAX_QUANTITY-1}: {e}")