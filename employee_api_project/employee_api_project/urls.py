"""
URL configuration for employee_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from employee import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('create/', views.create_employee_view, name='create_employee'),
    path('update/', views.update_employee_view, name='update_employee'),
    path('delete/', views.delete_employee_view, name='delete_employee'),
    path('get/', views.get_employee_view, name='get_employee'),
]
