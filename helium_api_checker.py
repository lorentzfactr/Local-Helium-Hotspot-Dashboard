#Written By: Lorentz Factr
#Date: 11/10/21

import requests
from datetime import datetime as d

#Time is date/time presented in iso format for two reasons:
#   1.The SQLite DB doesn't have a dedicated time format.
#   2.The Grafana DB visualization tool plugin requires this to read the read the value correctly from the DB.

class Retrieve:
    divisor = 100000000
    now = d.utcnow()
    time = now.isoformat("T")+"Z"

    def __init__ (self, hotspot_name, device_sn, api_key):
        self.hotspot_name = hotspot_name
        self.device_sn = device_sn
        self.api_key = api_key
        

    def hotspot_url(self):
        response = requests.get("https://api.helium.io/v1/hotspots/name/" + self.hotspot_name)
        return response.json()

    def account_url(self):
        response = requests.get("https://api.helium.io/v1/accounts/" + self.hotspot_url()['data'][0]['owner'])
        return response.json()

    def sensecap_url(self):
        sensecap_url = 'https://status.sensecapmx.cloud/api/openapi/device/view_device?sn='+ self.device_sn + '&api_key=' + self.api_key
        response = requests.get(sensecap_url)
        return response.json()

    def account_activity_url(self, min_time, bucket):
        # Min_time options: negative integers (in days)
        # Bucket options: hour, mins
        # Dict[‘data’][i][‘total’]
        # Dict[‘data’[i][‘timestamp’]

        url = 'https://api.helium.io/v1/accounts/' + self.hotspot_url()['data'][0]['owner'] + '/rewards/sum?min_time=' + min_time + '%20day&bucket=' + bucket
        return url
    
    def get_account_activity(self, min_time, bucket):
        response = requests.get(self.account_activity_url(min_time, bucket))
        rewards = response.json()
        rewards_list = []
        for i in range(abs(int(min_time))):
            list = []
            list.append(rewards['data'][i]['total'])
            list.append(rewards['data'][i]['timestamp'])
            rewards_list.append(list)
        return {'days': abs(int(min_time)),
                'bucket': bucket,
                'data' : rewards_list,
                }
    
    def recursive_lookup(self, k, d):
        if k in d:
            return d[k]
        for v in d.values():
            if isinstance(v, dict):
                return self.recursive_lookup(k, v)
        return None

    def market_price(self, symbol, metric):
        # Possible Metrics: 'name', 'symbol', 'priceUsd', 'priceBtc', 'percentChange24hUsd', 'lastUpdated'
        # Quotes from Binance
        #Build URL
        url = 'https://dev-api.shrimpy.io/v1/exchanges/binance/ticker?quoteTradingSymbol=' + symbol
        #Send HTTP Request 
        response = requests.get(url)
        market_data = response.json()
        # Filter the list with and return the dict of with symbols info
        c_dict = list(filter(lambda ticker: ticker['symbol'] == symbol, market_data))
        # Use recursive lookup to return the value of the metric key 
        return self.recursive_lookup(metric,c_dict[0]) 

    def get_hotspot_data(self):
        now = d.utcnow()
        time = now.isoformat("T")+"Z"
        hotspot_data = self.hotspot_url()
        account_data = self.account_url()
        quote = self.market_price('HNT', 'priceUsd')
        return self.organize_hotspot_data(hotspot_data,account_data, quote, time)

    def organize_hotspot_data(self, hotspot_data, account_data, quote, time):
        return {'owner': hotspot_data['data'][0]['owner'], 
                'block': hotspot_data['data'][0]['block'], 
                'block_added': hotspot_data['data'][0]['block_added'], 
                'lat': hotspot_data['data'][0]['lat'],
                'lng': hotspot_data['data'][0]['lng'], 
                'city': hotspot_data['data'][0]['geocode']['long_city'],
                'state': hotspot_data['data'][0]['geocode']['short_state'],
                'reward_scale': hotspot_data['data'][0]['reward_scale'],
                'gain': hotspot_data['data'][0]['gain'],
                'elevation': hotspot_data['data'][0]['elevation'],
                'wallet_balance': account_data['data']['balance']/self.divisor,
                'wallet_bal_USD': round(float(quote)*((int(account_data['data']['balance']))/self.divisor),2),
                'market_quote': quote,
                'time': time
                }
    def get_sensecap_data(self):
        data = self.sensecap_url()['data']
        now = d.utcnow()
        time = now.isoformat("T")+"Z"
        if data['connected'] == 1:
            data['connected'] = 'Healthy'
        if data['connected'] == 0:
            data['connected'] = 'Unhealthy'  
        if data['connected'] == -1:
            data['connected'] = 'Unknown' 
        if data['dialable'] == 1:
            data['dialable'] = 'Healthy'
        if data['dialable'] == 0:
            data['dialable'] = 'Unhealthy'  
        if data['dialable'] == -1:
            data['dialable'] = 'Unknown' 
        if data['natType'] == 3:
            data['natType'] = 'Restricted'
        if data['natType'] == 2:
            data['natType'] = 'Symmetric'  
        if data['natType'] == 1:
            data['natType'] = 'Static'
        if data['natType'] == 0:
            data['natType'] = 'None'  
        if data['natType'] == -1:
            data['natType'] = 'Unknown'
        if data['heliumOnline'] is True:
            data['heliumOnline'] = 'Online'  
        if data['heliumOnline'] is False:
            data['heliumOnline'] = 'Offline'
        if data['synced'] is True:
            data['synced'] = 'Yes'  
        if data['synced'] is False:
            data['synced'] = 'No'
        if data['online'] is True:
            data['online'] = 'Online'  
        if data['online'] is False:
            data['online'] = 'Offline'
        if data['relayed'] == 1:
            data['relayed'] = 'Yes'  
        if data['relayed'] == 2:
            data['relayed'] = 'No'
        
        return {'height': data['height'],
                'connected': data['connected'],
                'dialable': data['dialable'],
                'natType': data['natType'],
                'fan_temp': data['fan_status_list'][0]['temperature'],
                'cpuTemp': data['cpuTemperature'],
                'cpuUsed': data['cpuUsed'],
                'memoryUsed': data['memoryUsed'],
                'memoryTotal': data['memoryTotal'],
                'sdUsed': data['sdUsed'],
                'sdTotal': data['sdTotal'],
                'FWversion': data['version']['firmware'],
                'gain': data['gain'],
                'heliumOnline': data['heliumOnline'],
                'totalheight': data['totalHeight'],
                'synced': data['synced'],
                'online': data['online'],
                'relayed': data['relayed'],
                'collectTime': data['collectTime'],
                'time': time
        }


