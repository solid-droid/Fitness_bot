#Import Functions
from bs4 import BeautifulSoup 
from urllib.request import urlopen
from urllib.request import Request

#Search Parameters 
#pageNo='1'
#searchURL='dosa'

#Open and get link from search page
url = 'https://www.myfitnesspal.com/food/search?page='+ pageNo + '&search='+ searchURL
ureq = Request(url, headers={'User-Agent':'Mozilla/5.0'})
htmlPage = urlopen(ureq)
soup = BeautifulSoup(htmlPage.read(), 'lxml')
items = soup.find("div", class_="food_info")
url = 'https://www.myfitnesspal.com'+str(items.a["href"])

#Open 1st result page
ureq = Request(url, headers={'User-Agent':'Mozilla/5.0'})
htmlPage = urlopen(ureq)
soup = BeautifulSoup(htmlPage.read(), 'lxml')

# itemName = soup.find("div", class_="root-1W4Ez")
# itemQuestion = soup.find("h1", class_="title-1P2uF")
# print("????: "+itemQuestion.text)
itemName = soup.find("h3", class_="jss3 jss17 pageTitle-_5t9X")
itemCal = soup.find("h1", class_="title-cgZqW")
itemCarb = soup.find("h1", class_="carbohydrates-orw9p subtitle-7_FIi")
itemProtein = soup.find("h1",class_="protein-Eg08Q subtitle-7_FIi")
itemFat = soup.find("h1",class_="fat-lHyji subtitle-7_FIi")
print("Food Name: "+itemName.text)
print("Calories: "+itemCal.text)
print("Carbs: "+itemCarb.text)
print("Protein: "+itemProtein.text)
print("Fat: "+itemFat.text)

