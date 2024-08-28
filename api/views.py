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

from operator import itemgetter



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
        data12=ref.child("blogs").child(path).set(data)

        print(data12)   
        print("Blog created successfully")
        return JsonResponse({'message':'Blog created successfully'})
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Blog creation failed'})
    

@csrf_exempt
@api_view(['GET'])
def getblogs(request):
    try:
        data=ref.child("blogs").get()
        # print(data)

        if data is not None:
            blog_list=sorted(list(data.values()),key=itemgetter('timestamp'),reverse=False)
            print("Total Blogs : ",len(blog_list))
            
            blog_list=blog_list[::-1]
        
        else:
            blog_list=[]

        page_number=request.GET.get('page',1)

        print("current page number ",page_number)


        paginator=Paginator(blog_list,10)

        page_obj=paginator.get_page(page_number)

        blogs_json=json.loads(json.dumps(page_obj.object_list))

        response_data={
            "data":blogs_json,
            "page_number":page_obj.number,
            "total_pages":paginator.num_pages
        }

        return JsonResponse(response_data)
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Failed to fetch blogs'})


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

        try:

            data_views=db.child('views').child(id).get().val()
            views=data_views+1
            db.child('views').child(id).set(views)

        except Exception as e:
            print(e)

            db.child('views').child(id).set(1)
        data=db.child('blogs').child(id).get()
        

        if data is not None:
            data=data.val()
            data['message']="success"
            data['views']=db.child('views').child(id).get().val()

            return JsonResponse(data)
        else:
            return JsonResponse({'message':'Failed'},status=404)
        
    except Exception as e:

        print(e)
        return JsonResponse({'message':'Failed to fetch blog data'})
    
@csrf_exempt
@api_view(['GET'])
def getuserblogs(request,username):
    try:
        data=ref.child('blogs').get()
        
        data=blog_list=sorted(list(data.values()),key=itemgetter('timestamp'),reverse=False)

        user_blogs=[blog for blog in data if blog['username']==username]

        print(user_blogs.count)
        if user_blogs.count==0:
            return JsonResponse({'message':'User has no blogs'},status=404)

        if data is not None:
            print("none")
            user_blogs=list(user_blogs)

            print("User blogs ",user_blogs)
            print("Total Blogs : ",len(user_blogs))
            
            blog_list=user_blogs[::-1]
        
        else:
            blog_list=[]

        page_number=request.GET.get('page',1)

        print("current page number ",page_number)


        paginator=Paginator(blog_list,10)

        page_obj=paginator.get_page(page_number)

        blogs_json=json.loads(json.dumps(page_obj.object_list))

        response_data={
            "data":blogs_json,
            "page_number":page_obj.number,
            "total_pages":paginator.num_pages
        }

        return JsonResponse(response_data,safe=False)
    
    except Exception as e:
    
        print(e)
        return JsonResponse({'message':'Failed to fetch user blogs'})

@csrf_exempt    
@api_view(['POST'])
def followuser(request, username):
    try:
        data = json.loads(request.body.decode('utf-8'))
        follower = data['follower']

        followers_ref = db.child("users").child(username).child('followers')
        followers_data = followers_ref.get().val() or {}
        
        if username in followers_data:
            return JsonResponse({'message': 'Cannot follow yourself'})
        
        if follower in followers_data.values():
            return JsonResponse({'message': 'Already following'})

        db.child("users").child(username).child('followers').push(follower)
        db.child("users").child(follower).child('following').push(username)

        return JsonResponse({'message': 'Followed successfully'})

    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed to follow'}, status=500)


    
@csrf_exempt
@api_view(['POST'])
def unfollowuser(request, username):
    try:
        data = json.loads(request.body.decode('utf-8'))
        follower = data['follower']

        follows_ref=db.child("users").child(username).child('followers').get().val()

        if follows_ref is None:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        for key, value in follows_ref.items():
            if value == follower:
                db.child("users").child(username).child('followers').child(key).remove()
                break
        
        following_ref=db.child("users").child(follower).child('following').get().val()

        if following_ref is None:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        for key, value in following_ref.items():
            if value == username:
                db.child("users").child(follower).child('following').child(key).remove()
                break
            

        return JsonResponse({'message': 'Unfollowed successfully'})

    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed to unfollow'}, status=500)

    
@csrf_exempt
@api_view(['POST'])
def getuserprofiledata(request, username):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username_following = data.get('username_following', '')
        
        user_data = db.child('users').child(username).get().val()

        if user_data is not None:
            user_data['message'] = "success"
            try:
                # Fetch followers and following
                followers = db.child("users").child(username).child('followers').get().val() or {}
                following = db.child("users").child(username).child('following').get().val() or {}

                user_data['followers'] = followers
                user_data['following'] = following

                # Safely count followers and following
                user_data['total'] = len(followers)
                user_data['following_total'] = len(following)

            except Exception as e:
                print(e)
                user_data['followers'] = {}
                user_data['following'] = {}
                user_data['total'] = 0
                user_data['following_total'] = 0

            # Check if the current user is following the profile user
            user_data['is_following'] = username_following in followers.values()

            print(user_data)

            return JsonResponse(user_data)

        else:
            return JsonResponse({'message': 'User not found'}, status=404)

    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Failed'}, status=500)
