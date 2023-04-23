from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('allmylinks/', views.allmylinks, name='allmylinks'),
    path('timeline/', views.timeline, name='timeline'),
    path('contact/', views.contact, name='contact'),
    path('hire-me/', views.hireme, name='hireme'),
    path('hire/', views.hireme, name='hire'),
]