<?php
#
# AUTHOR: Marcus Siqueira
# Requirements:
#   - Php 7.1.1 or later
#   - Curl 8.4.0
# This PHP example send the data via post request to one of the APIs avaiable by Amicci. 
# It's a generic code, and simulates fictional number of data to be sent.
# The code iterates over a bunch of data and send a maximum number of data each time. The current maximum data
# per request is 20000.
# The number of the requests to the API will depend on the ammount of data, because it has to respect
# the maximum data per request. 
# The data should be grouped and send the maximum possible at once.

# Total number of itens, in that case it should come from a file/database etc. But in out example it will be a fixed number.
$MAX_DATA = 40000;
# Max itens per post request in the API
$MAX_QUANTITY = 20000;

# URL of the Seller API (follow Amicci official links for the API URL)
$URL = '';
# Authorization Token (provided by Amicci official webiste, available at https://platform.amicci.com.br/home)
$TOKEN = '';

#Verify if URL and TOKEN were provided
if ($URL == NULL or $TOKEN == NULL)
{
  print("Must provide a valid URL and a valid TOKEN");
  exit();
}

# Class object with the available fields
class Seller
{
  #Required
  public $id_seller = NULL;
  public $name = NULL;

  #Optional
  public $cnpj = NULL;

  public function __construct($id_seller, $name)
  {
    if (empty($id_seller))
      throw new Exception("Field id_seller is required");
    elseif (empty($name))
      throw new Exception("Field name is required");
    $this->id_seller = $id_seller;
    $this->name = $name;
  }
}

# Iterate over the max items available to sent
for ($i = 1; $i <= $MAX_DATA; $i = $i + $MAX_QUANTITY)
{
  # Iterate over the data, generating objects until reaching the MAX_QUANTITY per request
  $list_json = array();
  for ($j = 1; $j <= $MAX_QUANTITY; $j++)
  {
    # Create an object and push it into the array/list
    try
    {
      # Creating object with required fields
      $obj = new Seller($j+$i-1, "seller_name_".($j+$i-1));
      # Assign optional fields if available
      $obj->cnpj = "22019551000130";
      array_push($list_json, $obj);
    }
    catch (Exception $e) 
    {
      echo "Object " . ($j+$i-1) . " not constructed: $e";
    }
    
  }

  # Encode the array/list into a json pattern, witch is required.
  $fields_string = json_encode($list_json);

  # Initializes the CURl (responsible for the request) and sets the necessary values to it
  $curl = curl_init();
  curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'POST');
  curl_setopt($curl, CURLOPT_ENCODING, '');
  curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
  curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json',"Authorization: $TOKEN"));
  curl_setopt($curl, CURLOPT_MAXREDIRS, 20);
  curl_setopt($curl, CURLOPT_POSTFIELDS, $fields_string);
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
  # Max time in seconds the Curl will wait from the API. 180 seconds (3 minutes) by default (The data will be validated and processed and its a large data)
  curl_setopt($curl, CURLOPT_TIMEOUT, 180);
  curl_setopt($curl, CURLOPT_URL, $URL);
  # Need to set an user agent so that the server accepts the request
  curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)');

  try 
  {
    #The response of the API witch will be initialized with null value
    $response = NULL;
    echo "Sending data to $URL \n";
    $response = curl_exec($curl);
    sleep(3);
  } 
  catch (Exception $e) 
  {
    echo 'Exception: ',  $e->getMessage(), "\n";
  }

  if ($response == NULL)
  {
    echo "There was a problem receiving response from the API.\n";
    echo "Data NOT processed from " . $i . " to " . ($i + $MAX_QUANTITY-1) . " successfully.\n";
  }
  else
  {
    echo $response . "\n";
    echo "Data processed from " . $i . " to " . ($i + $MAX_QUANTITY-1) . " successfully.\n";
  }
  curl_close($curl);
}