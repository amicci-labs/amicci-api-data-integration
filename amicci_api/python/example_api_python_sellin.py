#
# AUTHOR: Juliana Teixeira
# Requirements:
#   - Python 3.9.2 or later
#   - requests:
#      - pip install requests
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
from datetime import date, timedelta

# Total number of itens, in that case it should come from a file/database etc. But in out example it will be a fixed number.
MAX_DATA = 40000
# Max itens per post request in the API
MAX_QUANTITY = 20000

# URL of the Sellin API (follow Amicci official links for the API URL)
URL = ""
# Authorization Token (provided by Amicci official webiste, available at https://platform.amicci.com.br/home)
TOKEN = ""

#Verify if URL and TOKEN were provided
if URL is None or TOKEN is None:
    print("Must provide a valid URL and a valid TOKEN")
    exit()

# Class object with the available fields
class Sellin:
    
    #Required
    date = None
    id_invoice = None
    id_product = None
    id_seller = None
    purchase_value_gross = None
    purchase_value_liquid = None
    quantity = None
    
    def __init__(self, date, id_invoice, id_product, id_seller, purchase_value_gross, purchase_value_liquid, quantity):
        if date is None:
            raise ValueError(f"Field date is required")
        if id_invoice is None:
            raise ValueError(f"Field id_invoice is required")
        if id_product is None:
            raise ValueError(f"Field id_product is required")
        if id_seller is None:
            raise ValueError(f"Field id_seller is required")
        if purchase_value_gross is None:
            raise ValueError(f"Field purchase_value_gross is required")
        if purchase_value_liquid is None:
            raise ValueError(f"Field purchase_value_liquid is required")
        if quantity is None:
            raise ValueError(f"Field quantity is required")
        self.date = date
        self.id_invoice = id_invoice
        self.id_product = id_product
        self.id_seller = id_seller
        self.purchase_value_gross = purchase_value_gross
        self.purchase_value_liquid = purchase_value_liquid
        self.quantity = quantity
        

# Iterates over the maximum number of items to send
for i in range(1, MAX_DATA + 1, MAX_QUANTITY):
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in range(1, MAX_QUANTITY + 1):
        # Creates an object and adds it to the list
        try:
            # Creating object with required fields
            obj = Sellin((date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), j+i-1, j+i-1, j+i-1, 30, 15, 10)
            list_json.append(obj.__dict__)
        except Exception as e:
            print(f"Object {j+i-1} not constructed: {e}")

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
            print(f"Data processed from {i} to {i + MAX_QUANTITY-1} successfully")
        else:
            print(f"Data NOT processed from {i} to {i + MAX_QUANTITY-1} successfully")              
        time.sleep(3)
    except Exception as e:
        print(f"Exception caught for on data {i} to {i + MAX_QUANTITY-1}: {e}")