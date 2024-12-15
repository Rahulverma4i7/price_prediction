"""
URL configuration for price_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
print("importing views ...")
from django.contrib import admin
from django.urls import path
# from price_bot.views import home_view, about_view
from . import views

urlpatterns = [
    # path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    # path('about/', about_view, name='about'),
    path('fetch-village/', views.fetch_village_details, name='fetch_village'),
    path('fetch-nearby/', views.fetch_nearby_restaurants, name='fetch_nearby'),
     path('fetch-busy-times/', views.fetch_busy_times, name='fetch_busy_times'),
    path('fetch-weather/', views.fetch_weather_data, name='fetch_weather'),
    path('display-all/', views.display_all_data, name='display_all_data'),
]
