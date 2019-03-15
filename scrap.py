#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:42:39 2019

@author: abhijith
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import soup
import google_scrap
import json
import pickle
import re

menu_dict=None
my_api_key ="AIzaSyCDjvWjDItyjd_Le9sFhddg-BeVtQkMy3o"
my_cse_id = "007475133352381266766:wnzczgtjf4s"

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
    
def getHotelUrl(search_text):
    final_url=google_scrap.getFinalUrl(search_text)
    return final_url

def getHotelMenu(url):
    raw_html=simple_get(url)
    menu=soup.getFullMenu(raw_html)
    return menu
    


def getMenu(search_text, city="kochi"): #import this function jeby
#    try:
#        menu =menu_dict[search_text]
#        return menu
#    except KeyError:
        
        url=getHotelUrl(search_text + " ".format(city))
        menu=getHotelMenu(url)
        return menu
    
#raw_html = simple_get('https://www.swiggy.com/kochi/aavi-ittys-panampily-nagar-panampilly-nagar')
#filename="swiggy"
#file = open(filename, 'wb')
#pickle.dump(raw_html, file)
#file.close()
#print(len(raw_html))  
    
#flags=re.IGNORECASE
def getVegList(menu):
   #veg_list=menu
   veg_list={}
   for i in menu.keys():
      n1=len(menu[i])
      for j in range(n1):
          subsect=menu[i][j]
          item=subsect.keys()
          for k in item:
           sub_list=subsect[k]
           for l in sub_list:
               name=list(l.keys())[0]
               name=name.replace(" ", "").lower()
               cost=list(l.values())[0]
               if(name.startswith("veg") or name.startswith("meal")):
                   veg_list[name]=cost
   return veg_list

def getDict(menu):
   global menu_dict
   food_list={}
   food_tuple=[]
   for i in menu.keys():
      n1=len(menu[i])
      for j in range(n1):
          subsect=menu[i][j]
          item=subsect.keys()
          for k in item:
           sub_list=subsect[k]
           for l in sub_list:
               name=list(l.keys())[0]
               name=name.replace(" ", "").lower()
               cost=list(l.values())[0]
               food_list[name]=cost
               food_tuple.append((name, cost),)
   menu_dict=food_list           
   return food_list, food_tuple
        

def getFoodItems(menu):
    if(menu_dict==None):
        _, _=getDict(menu)
        return list(menu_dict.keys())
    else:
        return list(menu_dict.keys())
def getItemByName(menu, itemname): 
    itemlist=[]
    if(menu_dict==None):
        _, _=getDict(menu)
    for i in menu_dict.keys():
        if(i.find(itemname)!=-1):
            itemlist.append((i, menu_dict[i]),)
    return itemlist       
            
            
            
# menu=getMenu("thaal kitchen")
# print(len(menu))
# itemlist=getItemByName(menu, "biryani")
# foood_list=getFoodItems(menu)
# print(foood_list)
# print(itemlist)
    
    
    

    
    


