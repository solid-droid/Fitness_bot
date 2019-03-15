from math import ceil
from bs4 import BeautifulSoup 
from urllib.request import urlopen
from urllib.request import Request
from fuzzywuzzy import fuzz

def calBurned(calCount=170,weight=70):
    #(calories/minute) = MET x weight (in kilograms)/60
    #MET w=3.5 c=5 r=8
    wTime = ceil(calCount*60/(3.5*weight))
    cTime = ceil(calCount*60/(5*weight))
    jTime = ceil(calCount*60/(8*weight))
    return [str(wTime) + " minutes", str(cTime) + " minutes", str(jTime) + " minutes"]


def findFood(searchURL):

    # Create HTML Soup    

    surl = 'https://www.myfitnesspal.com/food/search?page=1&search='+ searchURL.replace(" ","%20")
    ureq = Request(surl, headers={'User-Agent':'Mozilla/5.0'})
    searchSoup = BeautifulSoup(urlopen(ureq).read(), 'lxml')

    # Get list of items matching search

    flist = []
    mydivs = searchSoup.find_all("div", class_="food_info")
    for items in mydivs:
        flist.append((items.a.text,items.find("div", class_="nutritional_info").text))
    if flist == []:
        print("No Results")
        return -1

    # Fuzzy search and find best match

    maxRatio = 0
    maxItem = flist[0]
    for item in flist[::-1]:
        currentRatio=fuzz.ratio(searchURL.lower(),item[0].lower())
        if currentRatio >= maxRatio:
            maxRatio = currentRatio
            maxItem = item
    print("Search Term: " + searchURL + "\nClosest Match: " + maxItem[0])        

    # Get result and clean

    itemName = maxItem[0]
    itemNutrition = (' '.join(maxItem[1].split())).split(",")

    # Parse Output

    itemServ = itemNutrition[0][14:]
    itemCal = itemNutrition[1][11:]
    itemFat = itemNutrition[2][6:]
    itemCarb = itemNutrition[3][8:]
    itemProtein = itemNutrition[4][10:]
    
    print("Food Name: " + itemName)
    print("Calories: " + itemCal)
    print("Serving Size: " + itemServ)
    print("Carbs: " + itemCarb)
    print("Protein: " + itemProtein)
    print("Fat: " + itemFat)
    
    return [itemName, itemCal, itemCarb, itemFat, itemProtein, itemServ]