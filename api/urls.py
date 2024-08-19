from django.urls import path
from .views import createblog,getblogs


urlpatterns = [
    path('createblog/', createblog,name="createblog"),
    path('getblogs/', getblogs,name="getblogs"),
]
