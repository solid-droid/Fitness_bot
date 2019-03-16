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
    try:
        menu=soup.getFullMenu(raw_html)
        return menu
    except Exception:
        return None
    


def getMenu(search_text, city="kochi"): #import this function jeby
#    try:
#        menu =menu_dict[search_text]
#        return menu
#    except KeyError:
        
        url=getHotelUrl(search_text + " ".format(city))
        menu=getHotelMenu(url)
        if(menu==None):
            return None
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
          subsect=menu[i.replace(" ","").lower()][j]
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



def getSubset(menu):
    if(menu==None):
        return None
    subset_dict={}
    for i in menu.keys():
        subset_dict[i.replace(" ","").lower()]=[]
        for j in menu[i]:
            subset_dict[i].append(list(j.keys())[0])
    return subset_dict       
def getItems(subsect):
    subkey=list(subsect.keys())[0]
    itemarray=subsect[subkey]
    subset_dict={}
    for l in itemarray:
        name=list(l.keys())[0]
        name=name.replace(" ", "").lower()
        cost=list(l.values())[0]
        subset_dict[name]=cost
    return subset_dict    
        
def getPrice(search_item="mariot", dish_name="chickenbiryani"):
    menu=getMenu(search_item)
    if(menu==None):
        return None
    all_items, _=getDict(menu)
    print(all_items)
    dish_name=dish_name.replace(" ","").lower()

    maxRatio = 0
    maxItem = None

    for itemKey in all_items.keys():
      currentRatio=fuzz.ratio(dish_name,itemKey)

      if currentRatio == 100:
        return all_items[itemKey]

      if currentRatio >= maxRatio:
        maxRatio = currentRatio
        bestMatch = itemKey

    try:
        return all_items[bestMatch]
    except KeyError:
        return None
      
        

def getFoodItems(menu):
    if(menu==None):
        return None
    if(menu_dict==None):
        _, _=getDict(menu)
        return list(menu_dict.keys())
    else:
        return list(menu_dict.keys())
def getItemByName(menu, itemname): 
    itemlist=[]
    if(menu==None):
        return None
    if(menu_dict==None):
        _, _=getDict(menu)
    for i in menu_dict.keys():
        if(i.find(itemname)!=-1):
            itemlist.append((i, menu_dict[i]),)
    return itemlist       
def menuJson(search_item):
    menu=getMenu(search_item)
    menu=getDict(menu)
    filename="menu_json"
    filehandle=open(filename, "w")
    filehandle.write(json.dumps(menu))
    filehandle.close()
               
            
            
#menu=getMenu("thaal kitchen kakkanad")
#
#print(len(menu))
#itemlist=getItemByName(menu, "biryani")
#foood_list=getFoodItems(menu)
#print(foood_list)
#print(itemlist)
#subs=menu["maincourse"]
#sublist=getSubset(menu)
#print(sublist)
price=getPrice("ifthar", "chickenbiryani")
print(price)




    
    

    
    


