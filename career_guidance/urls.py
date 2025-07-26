"""
URL configuration for career_guidance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from core.views import router, download_report, quiz_page, dashboard_page, feedback_page
from core.api import register, login_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/download_report/', download_report, name='download_report'),
    path('quiz/', quiz_page, name='quiz_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('feedback/', feedback_page, name='feedback_page'),
]
