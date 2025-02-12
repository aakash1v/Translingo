"""
URL configuration for Translingo project.

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
from django.urls import path
from django.contrib import admin
from translation.views import user_login, logout_view, translate_page, registration, predict, download

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔹 Home & Login
    path('', user_login, name='home'),
    path('login/', user_login, name='user_login'),  # ✅ Now Django can find this
    path('logout/', logout_view, name='logout'),  # ✅ Ensure 'logout' view is mapped correctly

    # 🔹 Registration
    path('registration/', registration, name='registration'),

    # 🔹 File Processing
    path('predict/', predict, name='predict'),
    path('download/', download, name='download'),

    # 🔹 Translate
    path('translate/', translate_page, name='translate_page'),
]
