from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('reg/', views.register_page, name='registration'),

]
