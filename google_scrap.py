#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 19:37:53 2019

@author: abhijith
"""
from googleapiclient.discovery import build

my_api_key ="AIzaSyCDjvWjDItyjd_Le9sFhddg-BeVtQkMy3o"
my_cse_id = "007475133352381266766:wnzczgtjf4s"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def getFinalUrl(search_text):
    results = google_search(
        'swiggy {} menu'.format(search_text), my_api_key, my_cse_id, num=2)
    if(results.empty()):
        return None
    final_url=results[0]["link"]
    return final_url