Written By: LorentzFactr

Date: 11/14/2021

11/17/2021 Updates:

	- Improved error handling of bad API response. Only accepts status code 200 and doesn't kill program otherwise.
	- Reduced API load by only requesting https://api.helium.io/v1/hotspots/name/hotspots/name/... once instead of twice
	- Removed unnecessary "organizer" function and stuffed it into the return
	
11/14/2021 Update: added error checker in the event the API has bad response, no dict key or vals.

Backlog (To Do's):
1. ~~Manage exceptions for API disconnects~~  ~~(11/14 update should handle this. Still testing though...)~~ (11/17 update has resolved this)
2. Create config file so users only need to update a .txt with their unique info, instead of touching the code.
3. "pythonize" the folder structure... (ie: create __init__, run file, etc.). 
4. Turn the code into a .bat or executable.
5. Migrate code base to Raspberry Pi and turn that into local server that never shuts down.
6. Add BME280 (temp/hum) sensors to RPi for more data. Maybe a local webcam (would need to waterproof it).
7. VERY STRETCH GOAL: figure out a way to visual DB within the code. (Removes the need for user to setup DB visualization tool)

General System Overview:
1. Python scripts pull API data, organizes data, and put data into DB.
2. DB visualization tool pulls data from local DB and displays it on localhost:3000

Prequisites:
1. Sensecap M1 Helium hotspot with your status.sensecap login already setup. This is where you will get your device serial number and API key.
2. Sensecap M1 Helium hotspot connected to your local network. 
2. Grafana installed with SQLlite plugin (https://grafana.com/grafana/plugins/frser-sqlite-datasource/)
3. Python 3 installed with the following library: spllite3 

Usage:

***NOTE: Steps 1 & 2 are already done for you.***
1. Create DB in the folder with the Python scripts helium.db with tables: device, helium
2. Both tables need columns setup in the correct order. See return statements 
from def get_hotspot_data & def get_sensecap_data inside of helium_api_checker.py
3. In db_population.py update the strings with your information: hotspot_name, device_sn, api_key
4. Run db_population.py. This runs continuously to populate the DB so if you turn off your computer it will stop populating the DB.
5. Open Grafana via web browser http://[localhost-ip]:3000
6. Link helium.db data source to Grafana
7. Configure your dashboard however you like. This part you're on your own for now... and requires some basic knowledge SQLlite queries.
	
	Examples: 
		
		  SELECT cpuTemp,time FROM device
	
		  SELECT wallet_balance FROM helium 

Final Note: For continuous DB population without worry of shutting down, consider migrating this to a local Raspberry Pi with Grafana installed.
Run as for as long as you want to capture data.


(Windows) To view Grafana from local computer:
1. Open browser
2. Goto localhost:3000

(Windows) To view Grafana from remote computer on local network:
1. Open Windows Defender Firewall
2. Click Advanced Settings
3. Click Inbound Rules
4. Click New Rule
5. Rule Type: Port, click next
6. Rule Applys to: TCP
7. Specific local port: 3000
8. Allow the connection, click Next
9. Rule Applies: select Private only, click Next
10. Name: Grafana, Description: (optional), click Finish
11. Look up the localhost IP address on your network
12. From a remote computer browser goto, http://[localhost-ip]:3000

***WARNING THIS IS AN OPEN PORT DIRECT INTO YOUR NETWORK. DO NOT DO THIS.***
***I AM NOT RESPONSIBLE FOR VIRUSES, BROKEN COMPUTERS, OR MALWARE. I REPEAT, YOU SHOULD NOT DO THIS.*** 

(Windows) To view Grafana from remote computer from another network:
1. Open Windows Defender Firewall
2. Click Advanced Settings
3. Click Inbound Rules
4. Click New Rule
5. Rule Type: Port, click next
6. Rule Applys to: TCP
7. Specific local port: 3000
8. Allow the connection, click Next
9. Rule Applies: select Public, Private, and Domain, click Next
10. Name: Grafana, Description: (optional), click Finish
11. Open browser.
12. Goto Router settings, reserve your IP & port, and make your IP & port a DHCP server on TCP protocol
13. From a remote computer browser goto, http://[your-network-ip]:3000
