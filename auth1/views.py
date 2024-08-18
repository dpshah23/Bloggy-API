from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from pyrebase import pyrebase
from dotenv import load_dotenv
import os

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
def login(request):
    email=request.data['email']
    password=request.data['password']

    try:
        islogin=conn.sign_in_with_email_and_password(email,password)

        data={'email':email}

        db.child('activelogin').push(data)
        
        return JsonResponse({'message':'Login successful'})
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Login failed'})
    
@csrf_exempt
@api_view(['POST'])
def signup(request):
    email=request.data['email']
    password=request.data['password']
    name=request.data['name']

    try:
        islogin=conn.create_user_with_email_and_password(email,password)

        data={'name':name,'email':email}

        db.child('users').push(data)

        return JsonResponse({'message':'created'})
    except Exception as e:
        print(e)
        return JsonResponse({'message':'exists'})