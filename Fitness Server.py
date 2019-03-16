from flask import *
import json
from zomato import *
from mfp_search import*
from fuzzy_scrap import*
myWrapper=ZomatoWrapper(API_KEY)

text="none"
req=""
#########################################################---Exercise---###########################################
def exercise(val,num,brn,wt):
    if(val==""):
        if num==0:
            return "I coudn't find any recomandations."
        if(brn=="calories"):
            st = calBurned(num,wt)
        elif brn == "fat":
            st = calBurned(num*9,wt)
    else:
        val = val.title()
        dat = findFood(str(val))
        st  = calBurned(float(dat[1]),wt)

    return "You can burn the same by walking for "+str(st[0])+" , jogging for "+str(st[1])+" or just cycling for "+ str(st[2])

#####################################################---Diet---######################################################
def diet():

    return(text)
########################################################---Hotel---##################################################
def hotel(strng):
    strng=strng.split()
    location=strng[-1]
    location=location.capitalize()
    if(location=="Restaurants" or location=="Restaurant" or location=="Hotel" or location=="Hotels"):
        return ("Sorry no location was specified.")
    hotels, _=getTopRest(myWrapper,location )
    if(hotels==None):
        return("Sorry I could not find any results.")
    else:
        return ("Some of the top rated restaurants in the area are "+str(hotels[0])+", "+str(hotels[1])+" and "+str(hotels[2]))
##############################################################---food---##############################################

def food(val,cal):
    val=val.title()
    print(val)
    try:
        dat = findFood(str(val))
        cal=cal/3
        print(dat[1])
        if float(dat[1]) < cal:
            return "The " + str(dat[0]) + " consist of " + str(dat[1]) + " Calories a serving, which goes fine with your diet plan"
        else:
            return "The " + str(dat[0]) + " consist of " + str(dat[1]) + " Calories a serving, you must restrict your food intake to follow your diet plan"
    except:
        return "Sorry no such item found."


##################################################################---Food Conent---##################################
def calo(val,typ):
    val = val.title()
    print(val)
    dat = findFood(str(val))
    if(typ=="calories"):
        return str(dat[0]) + " contains " + str(dat[1]) +" calories"
    if(typ=="carb"):
        return str(dat[0]) + " contains " + str(dat[2]) +" carbs"
    if(typ=="fat"):
        return str(dat[0]) + " contains " + str(dat[3]) +" fat"
    if(typ=="protein"):
        return str(dat[0]) + " contains " + str(dat[4]) +" protein"
    return "Sorry nothing matching was found."
#############################################################---Menu---##############################################
def menu(hotel_name,val):
    ttt=val.capitalize()
    val=val.replace(" ","")
    print(val)
    cst=getPrice(str(hotel_name),str(val))
    if(cst==None):
        return "No such dish was found "
    else:
        return ttt+" cost "+str(cst)+"Rs at "+ hotel_name
###############################################################----HTTP SECTION---####################################
app = Flask(__name__)
def results():
    text="none"
    req = request.get_json(force=True)
    print(req)
    intent = req.get('queryResult').get('intent').get('displayName')
####################################################################################
    if intent == "Exercise" :
        fd=""
        num=0
        brn=""
        if req.get('queryResult').get('parameters').get('Burn'):
            brn = req.get('queryResult').get('parameters').get('Burn')
        if(req.get('queryResult').get('parameters').get('number')):
            num = req.get('queryResult').get('parameters').get('number')
        if req.get('queryResult').get('parameters').get('food'):
            fd  = req.get('queryResult').get('parameters').get('food')
        wt=int(req.get('queryResult').get('parameters').get('unit-weight').get('amount'))
        text = exercise(fd,num,brn,wt)
####################################################################################
    if intent == "Restaurant":
        text = hotel(req.get('queryResult').get('queryText'))
####################################################################################
    if intent == "Food":
        num = req.get('queryResult').get('parameters').get('number')
        fd  = req.get('queryResult').get('parameters').get('food')
        text = food(fd,num)

##################################################################################
    if intent == "Menu":
        h1 = req.get('queryResult').get('parameters').get('hotel')
        fd = req.get('queryResult').get('parameters').get('food')
        text = menu(h1,fd)
##################################################################################
    if intent == "Diet":
        text = diet()
##################################################################################
    if intent == "calorie":
        num = req.get('queryResult').get('parameters').get('Burn')
        fd = req.get('queryResult').get('parameters').get('food')
        text = calo(fd,num)

    # action = req.get('queryResult').get('action')
    # param = req.get('queryResult').get('parameter')

    print(text)
    return {'fulfillmentText': text}

@app.route('/assist', methods=['POST'])

def static_res():
    return make_response(jsonify(results()))
if __name__ == '__main__':
    app.run()