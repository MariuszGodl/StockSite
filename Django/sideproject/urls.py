"""
URL configuration for sideproject project.

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
from django.urls import path, re_path
from stocks.views import company_detail, contact, about_me


urlpatterns = [
    path('admin/', admin.site.urls),
     path("company/", company_detail, name="company_detail"),
    path("company/<str:identifier>/", company_detail, name="company_detail"),
    path("contact/", contact, name="contact"),
    path("aboutme/", about_me, name="about_me"),


    re_path(
        r'^company/(?P<identifier>\w+)/(?P<value_date>\d{4}-\d{2}-\d{2})/$',
        company_detail,
        name="company_detail_with_date"
    ),
]
