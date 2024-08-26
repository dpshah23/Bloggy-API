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
from django.shortcuts import render


import json
import re
import base64
import firebase_admin

from firebase_admin import credentials, storage, db

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
cred=credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': config['storageBucket'],
    'databaseURL': config['databaseURL']
})

ref=db.reference()

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
            "title": title, 
            "content": content,
            "username": username,
            "email": email,
            "image": image_url,
            "timestamp": timestamp,
            "id": id1
        }
        path =id1
        db.child("blogs").child(path).set(data)
        return JsonResponse({'message':'Blog created successfully'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Blog creation failed'})
    

@csrf_exempt
@api_view(['GET'])
def getblogs(request):
    try:
        data = ref.child("blogs").get()
        print(data)

        if data is not None:
            blog_list = list(data.values())
        else:
            blog_list = []

       
        page_number = request.GET.get('page', 1)
        print("page number ", page_number)

        paginator = Paginator(blog_list, 10)

        try:
          
            page_obj = paginator.page(page_number)
        except EmptyPage:
            
            page_obj = []

       
        blogs_json = json.loads(json.dumps(page_obj.object_list))

        response_data = {
            "data": blogs_json,
            "page_number": page_obj.number if blogs_json else page_number,
            "total_pages": paginator.num_pages
        }

        return JsonResponse(response_data)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed to fetch blogs'}, status=500)

@csrf_exempt
@api_view(['POST'])
def profile(request,username):
    try:
        data=db.child('users').child(username).get().val()
        

        if data is not None:
            
            data['message']="success"
            
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'message':'User not found'},status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Failed'})
    

@csrf_exempt
@api_view(['POST'])
def getblog(request,id):
    try:
        print("Blog id :",id)
        data=db.child('blogs').child(id).get().val()
        
        print(data)

        if data is not None:
           
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({'message':'Blog not found'},status=404,safe=False)
        
    except Exception as e:

        print(e)
        return JsonResponse({'message':'Failed to fetch blog data'},safe=False)
    
@csrf_exempt
@api_view(['POST'])
def getuserblogs(request,username):
    try:
        data=db.child('blogs').get()

        blog_list=list(data.values())
        
        user_blogs=[blog for blog in blog_list if blog['username']==username]

        return JsonResponse(user_blogs,safe=False)
    
    except Exception as e:
    
        print(e)
        return JsonResponse({'message':'Failed to fetch user blogs'})
    
