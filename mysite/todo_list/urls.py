from django.urls import path
from . import views
urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('delete/<list_id>', views.delete, name='delete'),
   path('cross_off/<list_id>', views.cross_off, name='cross_off'),
   path('uncross/<list_id>', views.uncross, name='uncross'),
   path('edit/<list_id>', views.edit, name='edit'),
   path('show_image/', views.show_image, name='show_image'),
   path('my_django_form/', views.my_django_form, name='my_django_form'),
   path('person/', views.person, name='person'),
   path('register/', views.register, name='register'),
   path('special/', views.special, name='special'),
   path('logout/', views.user_logout, name='logout'),
   path('user_login/', views.user_login, name='user_login'),
   path('cbview/', views.CBView.as_view(), name='CBView'),
]
