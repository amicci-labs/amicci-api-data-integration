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

# URL of the Sellout API (follow Amicci official links for the API URL)
URL = ""
# Authorization Token (provided by Amicci official webiste, available at https://platform.amicci.com.br/home)
TOKEN = ""

#Verify if URL and TOKEN were provided
if URL is None or TOKEN is None:
    print("Must provide a valid URL and a valid TOKEN")
    exit()

# Class object with the available fields
class Sellout:

    #Required
    date = None
    id_product = None
    id_store = None
    quantity = None
    sale_gross = None
    sale_liquid = None
    

    #Optional
    cost_gross = None
    cost_liquid = None
    sale_channel = None

    def __init__(self, date, id_product, id_store, quantity, sale_gross, sale_liquid):
        if date is None:
            raise ValueError(f"Field Date is required")
        if id_product is None:
            raise ValueError(f"Field id_product is required")
        if id_store is None:
            raise ValueError(f"Field id_store is required")
        if quantity is None:
            raise ValueError(f"Field quantity is required")
        if sale_gross is None:
            raise ValueError(f"Field sale_gross is required")
        if sale_liquid is None:
            raise ValueError(f"Field sale_liquid is required")
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
            # Creating object with required fields
            obj = Sellout((date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), j+i-1, j+i-1, 15, 30, 20)
            # Assign optional fields if available
            obj.cost_gross = "25"
            obj.cost_liquid = "15"
            obj.sale_channel = "online"
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