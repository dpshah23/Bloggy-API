from django.urls import path
from .views import createblog


urlpatterns = [
    path('createblog/', createblog,name="createblog"),
]
