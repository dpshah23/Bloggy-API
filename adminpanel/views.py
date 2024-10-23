from django.shortcuts import render,redirect
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.

def index(request):

    if 'email' in request.session:
        return render(request, 'dashboard.html')

def dashboard(request):
    
        if 'email' in request.session:
            return render(request, 'dashboard.html')
        else:
            return render(request, 'login.html')
        
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