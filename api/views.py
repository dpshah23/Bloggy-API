# import datetime
from io import BytesIO
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from pyrebase import pyrebase
from dotenv import load_dotenv
import os
from django.http import JsonResponse
from datetime import datetime

import string
import random

import json
import re
import base64

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

bucket=firebase.storage()
db=firebase.database()
print(conn)
print(db)

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def createblog(request):
    
    try:
        # print("Raw request body:", request.body.decode('utf-8'))
        
        data = json.loads(request.body.decode('utf-8'))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = json.loads(request.body.decode('utf-8'))

        # print(data)
        
        title = data.get('title')
        content = data.get('content')
        username = data.get('username')
        email = data.get('email')
        image = data.get('image')

        sanitized_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')

        sanitized_content = re.sub(r'[^\w\s-]', '', content).strip().replace(' ', '_')


        id1=''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        data={'id':id1,'title':title,'content':content,'username':username,'timestamp':timestamp,'email':email,'image':image}

        image_url=None

        try:

            
            image_data = base64.b64decode(image)
        
            
            image_name =''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

            bucket.child(image_name).put(BytesIO(image_data))
            image_url = bucket.child(image_name).get_url(None)


        except Exception as e:
            print(f"Image decoding error: {e}")
            return JsonResponse({'message': 'Invalid image data'}, status=400)
        
        data={
            "title": sanitized_title, 
            "content": sanitized_content,
            "username": username,
            "email": email,
            "image": image_url,
            "timestamp": timestamp,
            "id": id1
        }
        db.child('blogs').child(f"{title} by {username}").set(data)
        return JsonResponse({'message':'Blog created successfully'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Blog creation failed'})
    