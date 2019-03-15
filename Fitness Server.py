from flask import *
import json
text="none"
req=""
def exercise():

    return(text)

def diet():
    return(text)

def hotel():
    return(text)

def food():
    return(text)

def recipi():
    return(text)



app = Flask(__name__)
def results():
    req = request.get_json(force=True)
    intent = req.get('queryResult').get('intent').get('displayName')
    if intent is "Exercise" :
        exercise()
    if intent is "Diet":
        diet()
    if intent is "Restaurant":
        hotel()
    if intent is "Food":
        food()
    if intent is "Recipi":
        recipi()

    action = req.get('queryResult').get('action')
    param = req.get('queryResult').get('parameter')
    print(intent);
    action = req.get('queryResult').get('action')
    speech = "The interest rate of "
    return {'fulfillmentText': speech}

@app.route('/assist', methods=['POST'])

def static_res():
    return make_response(jsonify(results()))
if __name__ == '__main__':
    app.run()