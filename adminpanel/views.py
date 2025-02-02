from django.shortcuts import render,redirect
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from datetime import datetime
import string
import random
from pyrebase import pyrebase
from operator import itemgetter


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

load_dotenv()

firebase = pyrebase.initialize_app(config)
conn = firebase.auth()

bucket=firebase.storage()
db=firebase.database()
print(conn)

# Create your views here.

def index(request):

    if 'email' in request.session:
        return render(request, 'dashboard.html')

def dashboard(request):
    if 'email' not in request.session:
        return redirect('/adminpanel/login/')

    total_users = db.child('users').shallow().get().val()
    total_users_len = len(total_users) if total_users else 0

    total_blogs = db.child('blogs').shallow().get().val()
    total_blogs_len = len(total_blogs) if total_blogs else 0
    
    data = db.child('blogs').get().val()

    if data is not None:
        blog_list = sorted(list(data.values()), key=itemgetter('timestamp'), reverse=False)
        print("Total Blogs: ", len(blog_list))
        
        blog_list = blog_list[::-1]
        print(blog_list)

        for blog in blog_list:
            views = db.child('views').child(blog['id']).shallow().get().val()
            blog['decoded_content'] = decodebase64(blog['content'])  # Decode content
            blog['views'] = views if views is not None else 0  # Default to 0 if no views


        max_viewed_blogs = sorted(blog_list, key=itemgetter('views'), reverse=True)[:5]

        context = {
            'total_users': total_users_len,
            'total_blogs': total_blogs_len,
            'blog_list': blog_list,
            'max_viewed_blogs': max_viewed_blogs
        }
        print(context)
    else:
        blog_list = []

    return render(request, 'dashboard.html', context)


        
def login(request):

    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, password)

        print(os.getenv('EMAIL_ADMIN'), os.getenv('PASSWORD_ADMIN'))
        if email==os.getenv('EMAIL_ADMIN') and password==os.getenv('PASSWORD_ADMIN'):
            
            request.session['email'] = email
        
            return redirect('/adminpanel/dashboard/')
        
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('/adminpanel/login/')

def decodebase64(data):
    return data.encode('ascii')