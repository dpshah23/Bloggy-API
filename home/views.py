from django.shortcuts import render
import pyrebase
from pyrebase import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "apiKey": os.getenv('apikey'),
    "authDomain": os.getenv('authDomain'),
    "projectId": os.getenv('projectId'),
    "storageBucket": os.getenv('storageBucket'),
    "messagingSenderId": os.getenv('messagingSenderId'),
    "appId": os.getenv('appId'),
    "measurementId": os.getenv('measurementId'),
    "databaseURL": os.getenv('databaseURL')
}


firebase = pyrebase.initialize_app(config)

db=firebase.database()

# Create your views here.
def page(request,username):

    background=request.GET.get('theme','light').lower()
    total=request.GET.get('total',3)
    max_width=request.GET.get('max_width',846)
    max_height=request.GET.get('max_height',300)


    data=db.child('blogs').get().val()

    final=[]
    len=0
    for i in data:
        
        if len==total:
            break

        if data[i]['username']==username:
            final.append(data[i])
            len+=1
        

    return render(request,'blogs.html',{'blogs':final,'background':background,'max_width':max_width,'min_height':max_height})