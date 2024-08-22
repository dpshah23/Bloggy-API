import string
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import pyrebase
from pyrebase import pyrebase
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pyrebase.pyrebase import storage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random
import smtplib
from PIL import Image, ImageDraw, ImageFont
import io


# Create your views here.



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

        avatar_image = avatar(email)
        avatar_name = f"{username}.png"

        imagepush=bucket.child("avatars").child(avatar_name).put(avatar_image)

        avatar_url = bucket.child("avatars").child(avatar_name).get_url(None)
        

        islogin = conn.create_user_with_email_and_password(email, password)

        paylaod = {'name': name, 'email': email, 'username': username, 'phone':phone , 'avatar': avatar_url}

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
                    email=emails.val()['email']
                    email_exists=True
                    break
                else:
                    email_exists=False

            if email_exists:
                x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
                print(email_exists)
                print(email)
                print("email sent")

                emaiid=os.getenv('email')
                password=os.getenv('password')

                print(email)

                title="Password reset Request"

                final_str_link=""

                body=f"""
                <h1>Password reset request</h1>
                
                div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="text-align: center; color: #4CAF50;">Password Reset Request</h1>

                <p>Dear User,</p>

                <p>We understand that you are having trouble logging into your Bloggy account. To help you get back on track, we have received a request to reset your password.</p>

                <p>If you initiated this request, you can reset your password by clicking the link below. For security reasons, this link will expire in 1 hour:</p>

                <div style="text-align: center; margin: 20px 0;">
                    <h2 style="display: inline-block; background: #f4f4f4; padding: 10px 20px; border: 1px solid #ddd; border-radius: 5px;">
                <a href="{final_str_link}" style="text-decoration: none; color: #4CAF50;">Reset Password</a>
                    </h2>
                </div>

                <p>If you did not request a password reset, please ignore this message. Your account will remain secure, and no changes will be made.</p>

                <p>If you have any questions or need further assistance, please do not hesitate to contact our team.</p>

                <p>Thank you for your understanding and cooperation.</p>

                <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
                </div>
            

                """

                msg=MIMEMultipart()
                msg['From']=emaiid
                msg['To']=email
                msg['Subject']=title

                msg.attach(MIMEText(body,'html'))

                text=msg.as_string()

                server=smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(emaiid,password)
                server.sendmail(emaiid,email,text)
                server.quit()

                expiry_duration = timedelta(hours=1)
                expiry_time = datetime.now() + expiry_duration

                

                db.child('passwordreset').push({'email':email,'expiry':expiry_time.strftime('%Y-%m-%d %H:%M:%S')})

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
    

def avatar(email,size=128):
    image = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(image)

    circle_color = tuple(random.randint(0, 255) for _ in range(3))
    draw.ellipse([(0, 0), (size, size)], fill=circle_color, outline=None)

    text = email[0].upper()
    font_size = size // 2
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) / 2
    text_y = (size - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill='white')

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()