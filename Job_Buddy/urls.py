"""
URL configuration for Job_Buddy project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Base.urls')),
    path('admin_app', include('Admin_Management.urls')),
    path('Post', include('Post.urls')),
    path('chat', include('chat.urls')),
    path('Ticket_Management', include('Ticket_Management.urls')),
    path('Job_Management', include('Job_Management.urls')),
    path('Alumni', include('Alumni.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
