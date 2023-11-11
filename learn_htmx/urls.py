"""
URL configuration for learn_htmx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from returnapp import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('form/', TemplateView.as_view(template_name='form.html'), name='form'),
    path('admin/', admin.site.urls),
    path('return/', views.home, name='home'),
    path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
    path('', include('security.urls')),
]
