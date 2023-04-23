from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='PortfolioHome'),
    path('<str:slug>/', views.portfolio_item, name='PortfolioItem'),
]