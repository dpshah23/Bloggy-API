from django.urls import path
from .views import page


urlpatterns = [
    path('blogs/<str:username>/', page, name='blogs'),

]
