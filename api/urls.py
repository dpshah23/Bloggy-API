from django.urls import path
from .views import createblog,getblogs,profile,getblog,getuserblogs,getuserprofiledata,unfollowuser,followuser


urlpatterns = [
    path('createblog/', createblog,name="createblog"),
    path('getblogs/', getblogs,name="getblogs"),
    path('profile/<str:username>/', profile,name="profile"),
    path('getblog/<str:id>/', getblog,name="getblog"),
    path('getuserblog/<str:username>/', getuserblogs,name="getuserblog"),
    path('getuserprofile/<str:username>/', getuserprofiledata,name="getuserprofile"),
    path('unfollowuser/<str:username>/', unfollowuser,name="unfollowuser"),
    path('followuser/<str:username>/', followuser,name="followuser"),

]
