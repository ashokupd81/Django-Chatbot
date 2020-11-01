from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    #url(r'^$',views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    #url(r'^$', views.Home, name='home'),
    url(r'^post/$', views.Post, name='post'),
]