#
# AUTHOR: Marcus Siqueira
# Requirements:
#   - Ruby 3.2.3
#   - rest-client:
#      - gem install ffi
#      - gem install rest-client
# This Ruby example send the data via post request to one of the APIs avaiable by Amicci. 
# It's a generic code, and simulates fictional number of data to be sent.
# The code iterates over a bunch of data and send a maximum number of data each time. The current maximum data
# per request is 20000.  
# The number of the requests to the API will depend on the ammount of data, because it has to respect
# the maximum data per request. 
# The data should be grouped and send the maximum possible at once.

require 'json'
require 'rest-client'

# Total number of itens, in that case it should come from a file/database etc. But in out example it will be a fixed number.
MAX_DATA = 40000
# Max itens per post request in the API
MAX_QUANTITY = 20000

# URL of the Seller API (follow Amicci official links for the API URL)
URL = ""
# Authorization Token (provided by Amicci official webiste, available at https://platform.amicci.com.br/home)
TOKEN = ""

#Verify if URL and TOKEN were provided
if URL == "" or TOKEN == ""
    puts "Must provide a valid URL and a valid TOKEN"
    exit()
end

# Class object with the available fields
class Seller
    
    #Required
    attr_accessor :id_seller, :name

    #Optional
    attr_accessor :cnpj

    def initialize id_seller, name
        if id_seller.nil?
            raise "Field id_seller is required"
        elsif name.nil?
            raise "Field name is required"
        end
        @id_seller = id_seller
        @name = name
    end
end

# Iterates over the maximum number of items to send
for i in (1..MAX_DATA).step(MAX_QUANTITY)
    # Iterates over the data, generating objects until reaching the MAX_QUANTITY per request
    list_json = []
    for j in (1..MAX_QUANTITY).step(1)
      # Creates an object and adds it to the list
        begin
            # Creating object with required fields
            obj = Seller.new(j+i-1, "seller_name_#{j + i - 1}")
            # Assign optional fields if available
            obj.cnpj = "22019551000130"
            list_json << obj.instance_variables.map { |var| [var.to_s.delete('@'), obj.instance_variable_get(var)] }.to_h
        rescue => e
            puts "Object #{j+i-1} not constructed: #{e}"
        end
    end
    # Converts the list to JSON format, which is required
    fields_string = list_json.to_json
    begin
        headers = { "Content-Type" => "application/json", "Authorization" => TOKEN }
        puts "Sending data to #{URL}"
        response = RestClient.post(URL, fields_string, headers)
        if response.code == 200 || response.code == 201
            puts response.body
            puts "Data processed from #{i} to #{i+MAX_QUANTITY-1} successfully"
        else
            puts "Data NOT processed from #{i} to #{i+MAX_QUANTITY - 1} successfully"
        end
        sleep(3)
    rescue => e
        puts "Exception caught for on data #{i} to #{i+MAX_QUANTITY-1}: #{e}"
    end
end


