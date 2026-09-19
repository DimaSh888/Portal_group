from django.urls import path
from portal_group import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('forum/', views.forum, name='topic_list'),
    path('advertisement/', views.advertisement, name='advertisement'),
    path('advertisement/create/', views.create_advertisement, name='create_advertisement'),
]
