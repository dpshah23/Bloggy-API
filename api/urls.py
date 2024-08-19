from django.urls import path
from .views import createblog,getblogs,profile


urlpatterns = [
    path('createblog/', createblog,name="createblog"),
    path('getblogs/', getblogs,name="getblogs"),
    path('profile/<str:username>/', profile,name="profile"),
]
