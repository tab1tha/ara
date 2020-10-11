from wit import Wit
from datetime import date
import time
import random
entity_list={'paul\'s birthday' : date(1996,11,8),
             'defense' : date(2020,9,1)}
greetings={1 : "hey" , 
           2 : "hi"  ,
           3 : "hello" , 
           4 : "how can I help you"  ,
           5 : "Yo" , 
           6 : "😕"  ,
           7 : "🖖" , 
           8 : "👋"  ,
           9 : "👊" , 
           10 : "welcome to reality, were nothing ever happens as planned.The more you live, the more you realise that life is nothing other than pain, suffering and loneliness"  }

def get_date(entity='') :
    entit=entity.lower()
    print(entit+" is on the "+entity_list[entit].isoformat()) if entit in entity_list else print('I don\'t know')
    
def get_time(entity='') :
    print('Sorry, I don\'t know')
    
def get_current_time() :
    print(time.strftime("%H:%M"))

def get_location(entity='') :
    print('sorry, I don\'t know')
    
intent_list={'get_date' : get_date,
             'get_time' : get_time,
             'get_current_time' : get_current_time,
             'get_location' : get_location,}

def greet() :
    random.seed()
    i=random.randint(1,10)
    print(greetings[i])
    
def handle_intents(resp) :
    intent=resp['intents'][0]['name']
    entities=resp['entities']
    if intent in intent_list :
        if entities :
            for entity in entities :
                for i in entities[entity] :
                    intent_list[intent](i['value'])
        else :
            intent_list[intent]
    else :
        print("I dont know")
    
client=Wit(access_token='JO6XKLQFUXGIKTM6LVU4XMZM3RQQS74A')
sms=str(input("hi there\n>"))
i=0
while True:
    resp=client.message(msg=sms)
    if 'wit$greetings' in resp['traits'] :
        greet()
        i=1
    if resp['intents'] :
        handle_intents(resp)
        i=1
    if 'wit$bye' in resp['traits'] :
        print('bye')
        i=1
        break
    if i==0 :
        print("Sorry I don\'t understand")
    sms=str(input(">"))
