from django.urls import path
from web.views import index
from . import views


app_name = 'web'

urlpatterns = [
    path('',index,name="index"),
]