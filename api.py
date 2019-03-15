#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:51:42 2019

@author: abhijith
"""

import requests
import json

API_KEY="1a04b741e7be557279cf9a8748b7316d"

class Api(object):
    def __init__(self, USER_KEY, host="https://developers.zomato.com/api/v2.1",
                 content_type='application/json'):
        self.host = host
        self.user_key = USER_KEY
#        self.headers = {
#            "User-agent": "curl/7.43.0",
#            'Accept': content_type,
#            'X-Zomato-API-Key': self.user_key
#        }
        self.headers = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.user_key}

    def get(self, endpoint, params):
        url = self.host + endpoint + "?"
        for k,v in params.items():
            url = url + "{}={}&".format(k, v)
        url = url.rstrip("&")
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    
    
api=Api(API_KEY) 
res=api.get("cities", {"q":"kochi"})   
print(json.dumps(res, indent=4, sort_keys=True))
    
    