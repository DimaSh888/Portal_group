from django.urls import path
from portal_group import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('forum/', views.forum, name='topic_list'),
    path('advertisement/', views.advertisement, name='advertisement'),
    path('advertisement/create/', views.create_advertisement, name='create_advertisement'),
]
