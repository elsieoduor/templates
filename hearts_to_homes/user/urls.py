from django.urls import path
# from . import views
from .views import UserView, ChiefView,CreateAccountView

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('chief/', ChiefView.as_view(), name='chief'),
    path('register/', CreateAccountView.as_view(), name='login')
]

# urlpatterns = [
#   #default
#     path('home/', views.home, name='home'),
#     path('about/', views.about, name='about'),
#     path('contact/', views.contact, name='contact'),
#     path('events/', views.event, name='events'),
#     path('reviews/', views.reviews, name='reviews'),

#     #user part
#     path('login/', views.loginpage, name='login'),
#     path('register/', views.registerpage, name='register'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     #Children's Homes user functionality
#     path('children_homes/', views.children_homes, name='children_homes'),
#     path('children_homes/search/', views.children_search, name='search_children_homes'),
#     path('children_homes/<int:id>/', views.children_detail, name='children_home_detail'),
#     path('children_homes/<int:id>/submit_review/', views.submit_review, name='submit_review'),
#     path('children_homes/<int:id>/schedule_visit/', views.schedule_visit, name='schedule_visit'),
#     #Donations
#     path('donations/', views.donations, name='donations'),
#     path('children_homes/<int:id>/donate/', views.make_donations, name='make_donations'),

#     #chief part
#     path('chief_dashboard/', views.chief_dashboard, name='dashboard'),
#     path('chief_login/', views.chief_loginpage, name='login'),
#     path('chief_register/', views.chief_registerpage, name='register'),
#     #crud on users
#     path('users/', views.all_users, name='users'),
#     path('add_user/', views.add_user, name='add_user'),
#     #CRUD on homes
#     path('add_home', views.add_home, name='add_home'),
#     path('edit_home/<int:id>/', views.edit_home, name='edit_home'),
#     path('delete_home/<int:id>/', views.delete_home, name='delete_home'),
#     path('analytics/most_visited_home', views.most_visited_home, name='most_visited_home'),
#     path('analytics/most_in_need_home', views.most_in_need_home, name='most_in_need_home'),
    
# ]