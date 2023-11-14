"""
URL configuration for project project.

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
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home, name='home'),
    path('signUpUser/', views.signUp_User, name='signUpUser'),
    path('logout/', views.Logout, name='logout'),
    path('login/', views.Login, name='login') ,
    path('user/', views.UserPage, name='user') ,
    path('courses/<str:type>/', views.CoursesPage, name='couress') ,
    path('book/<int:id>/', views.BookingCorses, name='book') ,
    path('addTestimonial/', views.addTestimonial, name='addtestimonial') ,
    path('contact/', views.ContactPage, name='contact') ,
    path('teacher/<int:id>/', views.TeacherPage, name='teacherPage'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)