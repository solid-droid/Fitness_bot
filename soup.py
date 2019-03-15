#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:29:13 2019

@author: abhijith
"""

from bs4 import BeautifulSoup


def getItemList(section): # section or subsection
    itemlist=section.findAll("div", {"class":"_2wg_t"})
    return itemlist

def getSubsections(section):
    subsections=section.findAll("div", {"class":"_1Jgt5"})
    if(subsections==None or len(subsections)<1):
        return None
    return subsections
def getNamePrice(item):
    name=item.find("div", {"class":"jTy8b"}).string
    price=item.findAll("span", {"class":"bQEAj"})
    minprice=9999
    for i in price:
        if(int(i.string)<minprice):
            minprice=int(i.string)
    return name, minprice      

def getFullMenu(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    menu_dict=dict()
    sections=html.findAll("div", {"class": "_2dS-v"})
    #seclen=len(sections)
    #print("seclen: ", seclen)
    count=0
    for i in sections:
        #print("i is ", count)
        if count==0:
            count+=1
            continue
        #print("jaba ")  
        count+=1
        section_title=i.find("h2").string
        sub_list=[]
        subsections=getSubsections(i)
        
        if(subsections==None):
            itemlist=getItemList(i)
            #length=len(itemlist)
            #print("length of itemlist : ", length)
            itemarray=list()
            for j in itemlist:
                name, price=getNamePrice(j)
                itemdict=dict()
                itemdict[name]=price
                itemarray.append(itemdict)
            subdict={}
            subdict[section_title]=itemarray
            sub_list.append(subdict)
        else:
           #sublen=len(subsections)
           #print("sublen", sublen)
           for j in subsections:
            itemlist=getItemList(j)
            itemarray=[]
            subsectiontitle=j.find("h3").string
            for k in itemlist:
                name, price=getNamePrice(k)
                itemdict={}
                itemdict[name]=price
                itemarray.append(itemdict)
            subdict={}
            subdict[subsectiontitle]=itemarray
            sub_list.append(subdict)
        menu_dict[section_title]=sub_list
    return menu_dict
            
            
