from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from pyrebase import pyrebase
from dotenv import load_dotenv
import os
from datetime import datetime
from pyrebase.pyrebase import storage

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

        users = db.child('users').get()

        username = None

       
        for user in users.each():
            if user.val()['email'] == email:
                username = user.val().get('username')
                data['username'] = username
                break

        db.child('activelogin').push(data)

        print(username)

        return JsonResponse({'message':'Login successful','username':username})
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Login failed'})
    
@csrf_exempt
@api_view(['POST'])
def signup(request):
    email = request.data['email']
    password = request.data['password']
    name = request.data['name']
    username = request.data['username'] 
    phone=request.data['phone']

    try:
        # Check if the username already exists

        
        user = db.child("users").child(username).get()
        
        if user.val() is not None:
            return JsonResponse({'message': 'username_exists'})

        
        islogin = conn.create_user_with_email_and_password(email, password)

        paylaod = {'name': name, 'email': email, 'username': username, 'phone':phone}

        data = {'name': name, 'email': email, 'username': username}
        db.child('users').child(username).set(paylaod)

        return JsonResponse({'message': 'created'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'exists'})
    
@csrf_exempt
@api_view(['POST'])
def logout(request):
    email=request.data['email']

    try:
        db.child('activelogin').remove()

        return JsonResponse({'message':'Logout successful'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Logout failed'})
    

@csrf_exempt
@api_view(['POST'])
def forgetpass(request):
    
    email=request.data['email']

    try:
        try:
            email_exists=db.child('users').get()
            for emails in email_exists.each():
                if emails.val()['email'] == email:
                    email_exists=True
                    break
                else:
                    email_exists=False

            if email_exists:
                print(email_exists)
                print(email)
                print("email sent")

                return JsonResponse({'message':'Mail sent'})
            
            else:
                print("doesn't exist")
                return JsonResponse({'message':'Email not found'})
            
        except Exception as e:
            print(e)
            return JsonResponse({'message':'Email not found'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Password reset failed'})