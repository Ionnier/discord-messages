# pip install tzdata,requests,json
import requests,json
from types import SimpleNamespace
import datetime
import time
from zoneinfo import ZoneInfo
import os
try:
    from dotenv import load_dotenv,find_dotenv
    load_dotenv(find_dotenv(),verbose=True)
except ModuleNotFoundError:
    print("Dot env not found")

if os.getenv('CHANNEL_ID')==None:
    os.environ['CHANNEL_ID']=input('Enter your channel_id: ') 
if os.environ.get('AUTHOR_ID')==None:
    os.environ['AUTHOR_ID']=input('Enter your author_id: ')
if os.environ.get('AUTHORIZATION_ID')==None:
    os.environ['AUTHORIZATION_ID']=input('Enter your authorization_id: ')
if os.environ.get('YEAR_MESSAGE')==None:
    os.environ['YEAR_MESSAGE']=input('Enter your int YEAR_MESSAGE: ')
if os.environ.get('MONTH_MESSAGE')==None:
    os.environ['MONTH_MESSAGE']=input('Enter your int MONTH_MESSAGE: ')
if os.environ.get('DAY_MESSAGE')==None:
    os.environ['DAY_MESSAGE']=input('Enter your int DAY_MESSAGE: ')
if os.environ.get('MAX_ID')==None:
    os.environ['MAX_ID']=input('Enter your MAX_ID: ')

data_reper=datetime.date(int(os.environ.get('YEAR_MESSAGE')),int(os.environ.get('MONTH_MESSAGE')),int(os.environ.get('DAY_MESSAGE')))
numar_reper = int(os.environ.get('MAX_ID'))
diferenta=362387865600000

data_curenta = datetime.datetime.now(datetime.timezone.utc).astimezone(ZoneInfo(key='Europe/Bucharest')).date()
numar_reper=numar_reper+diferenta*((data_curenta-data_reper).days)

def find_key_days_ago(nr_zile):
    return numar_reper - nr_zile * diferenta

def build_request(channel_id,author_id,number_of_days):
    return "https://discord.com/api/v8/channels/"+str(channel_id)+"/messages/search?author_id="+str(author_id)+"&max_id="+str(find_key_days_ago(number_of_days))

zile=int(input('How many days ago shall we start?'))
data_curenta=data_curenta-datetime.timedelta(days=int(zile))

f = open("output.csv","w")
f.write("Data,Numar_Mesaje\n")
ok=1
print("If author_id is incorect, it will print all messages.")
while ok==1:
    try:
        r = requests.get(build_request(os.environ.get('CHANNEL_ID'),os.environ.get('AUTHOR_ID'),int(zile)), headers={"Authorization":os.environ.get('AUTHORIZATION_ID')})
        if r.status_code==404:
            x = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d))
            print(x.message)
            ok=0
            break
        if r.status_code==401:
            print("401: Unauthorized")
            ok=0
            break
        x = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d))
        print(str(data_curenta)+","+str(x.total_results))
        f.write(str(data_curenta)+","+str(x.total_results)+"\n")
        zile=zile+1
        data_curenta=data_curenta-datetime.timedelta(days=1)
        if(int(x.total_results)==0):
            f.close
            break
    except AttributeError:
        print("Attribute error, waiting")
        time.sleep(15)
    except KeyboardInterrupt:
        f.close
        ok=0
        
    

