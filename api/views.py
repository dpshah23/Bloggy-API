# import datetime
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from pyrebase import pyrebase
from dotenv import load_dotenv
import os
from django.http import JsonResponse
from datetime import datetime

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

print(config)

firebase = pyrebase.initialize_app(config)
conn = firebase.auth()
db=firebase.database()
print(conn)
print(db)

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def createblog(request):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = request.data['title']
        content = request.data['content']
        username=request.data['username']
        email=request.data['email']
        image=request.data['image']
        data={'title':title,'content':content,'username':username,'timestamp':timestamp,'email':email,'image':image}

        db.child('blogs').child(f"{title} by {username}").set(data)
        return JsonResponse({'message':'Blog created successfully'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Blog creation failed'})
    