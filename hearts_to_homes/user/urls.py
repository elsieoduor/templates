from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.event, name='events'),
    path('reviews/', views.reviews, name='reviews'),

    #Children's Homes user functionality
    path('children_homes/', views.children_homes, name='children_homes'),
    path('children_homes/search/', views.children_search, name='search_children_homes'),
    path('children_homes/<int:pk>/', views.children_detail, name='children_home_detail'),
    path('children_homes/<int:childrenhome_id>/submit_review/', views.submit_review, name='submit_review'),
    path('children_homes/<int:childrenhome_id>/schedule_visit/', views.schedule_visit, name='schedule_visit'),

    #Donations
    path('donations/', views.donations, name='donations'),
    path('children_homes/<int:childrenhome_id>/donate/', views.make_donations, name='make_donations'),
]