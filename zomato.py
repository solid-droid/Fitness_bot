#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 23:18:01 2019

@author: abhijith
"""

import requests
import json
from pprint import pprint


API_KEY="1a04b741e7be557279cf9a8748b7316d"
BASE_URL="https://developers.zomato.com/api/v2.1/"

def getTopRest(wrapper, location, sort="rating",count=3):
    loc_details= wrapper.getLocationDetails(location)
    if(loc_details[0]==None):
        return None, None
    res_list=wrapper.getRestuarents(loc_details, count=count, sort=sort)
    if(res_list==None):
        return None, None
    titles=[]
    menu_urls=[]
    ids=[]
    res_list2=res_list["restaurants"]
    for i in res_list2:
        titles.append(i["restaurant"]["name"])
        menu_urls.append(i["restaurant"]["menu_url"])
        ids.append(i["restaurant"]["id"])
    return titles, menu_urls  
    

class ZomatoWrapper:
    API_KEY
    baseUrl="https://developers.zomato.com/api/v2.1/"
    city_dict={}
    def __init__(self, key):
        self.API_KEY=key
    def setParams(self, options, kwargs):
        params={}
        for key in options:
            if key in kwargs:
                params[key] = kwargs[key]
        return  params       
    def addParams(self, url, params):
        url=url+"&"
        for k,v in params.items():
                url = url + "{}={}&".format(k, v)
        url = url.rstrip("&")  
        return url
            
    def getCityIdByName(self, cityname):
        try:
            city_id=self.city_dict[cityname]
            return city_id
        except KeyError:
            
            url=BASE_URL + "cities?q={}".format(cityname)
            print(url)
            header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
            res=requests.get(url=url, headers=header)
            city_details=res.json()
            try:
                city_id = city_details["location_suggestions"][0]["id"]
            except IndexError:
                return -1
            else:
                self.city_dict[cityname]=city_id
                return city_id

    def getCollections(self, city_id):
        count=50
        url=BASE_URL + "collections?city_id={}&count={}".format(city_id, count)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            collections=res.json()
            return collections
        else:
            return None
    def getCuisines(self, city_id):
        url=BASE_URL + "cuisines?city_id={}".format(city_id)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            cuisines=res.json()
            return cuisines["cuisines"]
        else:
            return None  
    def getEstablishments(self, city_id):
        url=BASE_URL + "establishments?city_id={}".format(city_id)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            establishments=res.json()
            return establishments["establishments"]
        else:
            return None  
    def getMenu(self, restaurant_id):
        url=BASE_URL + "dailymenu?res_id={}".format(restaurant_id)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            menu=res.json()
            return menu
        else:
            return None
    def getResDetails(self, restaurant_id):
        url=BASE_URL + "restaurant?res_id={}".format(restaurant_id)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            res_details=res.json()
            return res_details
        else:
            return None  
    def getReviews(self, restaurant_id, **kwargs):
        options=["start", "count"]
        params=self.setParams(options, kwargs)
        url=BASE_URL + "reviews?res_id={}".format(restaurant_id)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        url=self.addParams(url, params)
        res=requests.get(url=url, headers=header)
        if(res.status_code==200):
            reviews=res.json()
            return reviews
        else:
            return None      
        
    
    def getLocationDetails(self, location_name):
        url=BASE_URL + "locations?query={}".format(location_name)
        print(url)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        location_details=res.json()
        try:
            location_id = location_details["location_suggestions"][0]["entity_id"]
            city_id = location_details["location_suggestions"][0]["city_id"]
            location_type = location_details["location_suggestions"][0]["entity_type"]
        except IndexError:
            return None, None, None
        else:
            return (location_id, location_type, city_id)
    
    def getRestuarents(self, location_details, **kwargs):
        location_id, location_type, city_id=location_details
        options = [
            "entity_id", "entity_type", "q", "start",
            "count", "lat", "lon", "radius", "cuisines",
            "establishment_type", "collection_id",
            "category", "sort", "order"]
        params=self.setParams(options, kwargs)
        url=BASE_URL + "search?entity_id={}&entity_type={}".format(location_id, location_type) 
        url=self.addParams(url, params)
        print(url)
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": self.API_KEY}
        res=requests.get(url=url, headers=header)
        restuarent_list=res.json()
        try:
            if(restuarent_list["results_found"]>0):
                return restuarent_list
            else:
                return None
        except KeyError:
            return None
        
    
    

myWrapper=ZomatoWrapper(API_KEY)
#cid=myWrapper.getCityIdByName("kochi")
#print("city id: ", cid)
#mycol=myWrapper.getCollections(9)
#print(mycol["collections"][0]["collection"]["title"])


#locdetails=myWrapper.getLocationDetails("edapally")
#reslist=myWrapper.getRestuarents(locdetails, count="2", sort="rating")
#print(locdetails)
#print(json.dumps(reslist, indent=4))

#reviews=myWrapper.getReviews("900533")
#print(json.dumps(reviews, indent=4))
#cuisines=myWrapper.getCuisines(9)
#print(json.dumps(cuisines, indent=4))
#establishments=myWrapper.getEstablishments(9)
#print(json.dumps(establishments, indent=4))

names, menu_urls=getTopRest(myWrapper, "thrikkakara", count=5)
print(names)
print(menu_urls)
#print(r_ids)

