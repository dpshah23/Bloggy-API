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
    
    if 'email'not in request.session:
            return redirect('/adminpanel/login/')
    
    total_users = db.child('users').shallow().get().val()
    total_users = len(total_users) if total_users else 0

    total_blogs= db.child('blogs').shallow().get().val()
    total_blogs = len(total_blogs) if total_blogs else 0
    
    data=db.child('blogs').get().val()

    if data is not None:
            blog_list=sorted(list(data.values()),key=itemgetter('timestamp'),reverse=False)
            print("Total Blogs : ",len(blog_list))
            
            blog_list=blog_list[::-1]
            print(blog_list)

            for blog in blog_list:
                 blog['views']=db.child('views').child(blog['id']).shallow().get().val()
                 blog['views']=len(blog['views']) if blog['views'] else 0
            max_viewed_blogs = sorted(blog_list, key=itemgetter('views'), reverse=True)[:5]
            
            context = {
                'total_users': total_users,
                'total_blogs': total_blogs,
                'blog_list': blog_list,
                'max_viewed_blogs': max_viewed_blogs
            }
    else:
            blog_list=[]
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