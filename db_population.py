# Written By: LorentzFactr
# Date: 11/17/21
# To Do: 
# 1. Make exceptions for API's that can't connect. Right now, script will exit if an API goes down.
#    Forcing you to restart the script and missing mins/hours/days of data...
# 2. Add "Create DB" function into Readme for user to paste into the code on the first run and create the DB.
#    Right now, the user must have a basic working knowledge of how to create a DB with tables and setup
#    columns properly for ingesting the data stream from the script. 
# 3. Add API error counter and send to data to DB.
  
import sqlite3
from helium_api_checker import Retrieve
import time

#Your Three Word Hotspot Name
hotspot_name = 'your-hotspot-name'

#Your Sensecap M1 Serial Number
device_sn = 'xxxxxxxxxxxxxxxxx'

#Your Sensecap API Key
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#Database update frequency in seconds
frequency = 120

#Instatiate the database
conn = sqlite3.connect('helium.db')
c = conn.cursor()

#Table names for DB
device_table = 'device'
helium_table = 'helium'

#Instatiate the API checker
get = Retrieve(hotspot_name, device_sn, api_key)

print("\n*****************************************************")
print("********** HELIUM API CHECK & DB POPULATOR **********")
print("**********         BY: LORENTZFACTR        **********")
print("*****************************************************")

#Update DB function
def update_DB(d,table):
    
    # Don't populate DB if there was a bad request response from the API
    if "Error:" in d:
        print("\nAPI response error, did not populate database.")
        return print(d)
    
    else:
        columns = ', '.join(d.keys())
        placeholders = ':'+', :'.join(d.keys())
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
        c.execute(query, d)
        conn.commit()
        print("DB updated with %s table data." % (table,))

def main():
    print("\n")
    update_DB(get.get_sensecap_data(), device_table)
    update_DB(get.get_hotspot_data(), helium_table)

    time.sleep(frequency)

if __name__ == "__main__":
    while True:
        main()




