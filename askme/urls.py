"""
URL configuration for askme project.

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
from django.urls import path
from app import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = ([
    path('', views.index, name= 'index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:s>', views.tag, name='tag'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('logout/', views.log_out, name = "logout"),
    path('profile/edit/', views.settings, name = "settings"),
])

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
