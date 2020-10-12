from flask import Flask,request
import requests
import credentials
from datetime import date
import time
import random

#token used by facebook page to access the webapp
verifytoken='1234'

#token given by facebook to be added to our responseto be able to use the bkaaieuaireu 
TOKEN='EAAiEn1AALuYBAF9r4ysLfTgrZA5hTpSTlUo7uDUbBV1iOiagLOmCCn9NAs9jQCxwbrI6zafrWge6isIiDcVwjW8ztH9fCmhZBzXxUQZBcThTxzceHZCefUQUZA5TnTL25vNJSrqSoAXYlmXCYnr10Bitkn5YBgGlb5YZCnhF1pGAV8X0iH8k0q'
# create a list of entitites
entity_list={'paul\'s birthday' : date(1996,11,8),
             'defense' : date(2020,9,1)}

#create a list of greetings
greetings={1 : 'hey' , 
           2 : 'hi'  ,
           3 : 'hello' , 
           4 : 'how can I help you'  ,
           5 : 'Yo' , 
           6 : '😕'  ,
           7 : '🖖' , 
           8 : '👋'  ,
           9 : '👊' , 
           10 : 'welcome to reality, were nothing ever happens as planned.The more you live, the more you realise that life is nothing other than pain, suffering and loneliness'  }

#define methods to handle the various intents
def get_date(entity='') :
    entit=entity.lower()
    return (entit+" is on the "+entity_list[entit].isoformat()) if entit in entity_list else ('I don\'t know when '+entit+' is')
    
def get_time(entity='') :
    return 'Sorry, I don\'t know'
    
def get_current_time() :
    return 'summer time'
    return time.strftime("%H:%M")

def get_location(entity='') :
    return 'sorry, I don\'t know'
# creaing a dictionary of intents to match the string recieved to a function   
intent_list={'get_date' : get_date,
             'get_time' : get_time,
             'get_current_time' : get_current_time,
             'get_location' : get_location,}

def greet() :
    random.seed()
    i=random.randint(1,10)
    return greetings[i]

#the function which parses the responses and handles the intent 
def handle_intents(resp) :
    intent=resp['intents'][0]['name']
    entities=resp['entities']
    if intent in intent_list :
        if entities :
            for entity in entities :
                for i in entities[entity] :
                    if 'value' in i:
                        return intent_list[intent](i['value'])
                    elif 'resolved' in i :
                        return intent_list[intent](i['resolved']['values'][0]['name'])
                    else :
                        return 'Sorry I don\'t know'
        else :
            return intent_list[intent]()
    else :
        return 'I dont know'
    
def takecare(resp) :
    if 'wit$greetings' in resp['traits'] :
        return greet()
        i=1
    if resp['intents'] :
        return handle_intents(resp)
        i=1
    if 'wit$bye' in resp['traits'] :
        return 'bye'
        i=1
 
# creating a flask object for our webapp and the various functions to handle the request 
app=Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello world from Flask'
    
@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token=request.args.get("hub.verify_token")
    print(verify_token)
    if verify_token==verifytoken:
        print('done')
        return request.args.get("hub.challenge") 
    return 'Unable to authorise.'

@app.route('/webhook',methods=['POST'])
def webhook_hande():
    useful_info=None
    out=request.get_json()
    sender_id = out['entry'][0]['messaging'][0]['sender']['id']
    if out['entry'][0]['messaging'][0]['message']
        useful_info=out['entry'][0]['messaging'][0]['message']
    print(useful_info)
    if useful_info :
        request_body = {'recipient': {'id': sender_id},'message': {"text":takecare(useful_info['nlp'])}}
        print(request_body)
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+TOKEN,json=request_body).json()
        return response
    return 'ok'
    
if __name__=='__main__':
    app.run(debug=True)
