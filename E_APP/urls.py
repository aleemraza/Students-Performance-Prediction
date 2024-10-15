from django.urls import path
from . import views

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('dashboard/', views.deshboard, name="dashboard"),
    path('testdata/', views.testdata, name="testdata"), 
    path('home/', views.home, name='home'),
    path('results/', views.results , name="results"),
    path('about/', views.about , name="about"),
    path('contact/', views.contact , name="contact"),
    path('logout/',views.LogoutPage,name='logout'),
    path('delete_student/<int:pk>/', views.delete_user , name="delete_user"),
]