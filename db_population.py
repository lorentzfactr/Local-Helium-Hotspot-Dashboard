#Written By: Lorentz Factr
#Date: 11/10/21
#To Do: 
# 1. Make exceptions for API's that can't connect. Right now, script will exit if an API goes down.
#    Forcing you to restart the script and missing mins/hours/days of data...
# 2. Add "Create DB" function into Readme for user to paste into the code on the first run and create the DB.
#    Right now, the user must have a basic working knowledge of how to create a DB with tables and setup
#    columns properly for ingesting the data stream from the script. 

import sqlite3
from helium_api_checker import Retrieve
import time

#Your Three Word Hotspot Name
hotspot_name = 'your-silly-name'

#Your Sensecap M1 Serial Number
device_sn = 'xxxxxxxxxxxxxxxxxx'

#Your Sensecap API Key
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#Database update frequency in seconds
frequency = 5

#Instatiate the database
conn = sqlite3.connect('helium.db')
c = conn.cursor()

#Table names for DB
device_table = 'device'
helium_table = 'helium'

#Instatiate the API checker
get = Retrieve(hotspot_name, device_sn, api_key)

#Update DB function
def update_DB(d,table):
    columns = ', '.join(d.keys())
    placeholders = ':'+', :'.join(d.keys())
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
    c.execute(query, d)
    conn.commit()


def main():
    update_DB(get.get_sensecap_data(), device_table)
    update_DB(get.get_hotspot_data(), helium_table)
    #conn.close()
    print("\nDB Updated...")
    time.sleep(frequency)

if __name__ == "__main__":
    while True:
        main()



