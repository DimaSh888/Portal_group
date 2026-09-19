from django.urls import path
from portal_group import views
from voting import views as voting_views

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
    path('polls/', voting_views.poll_list, name='poll_list'),
    path('polls/<int:poll_id>/', voting_views.poll_detail, name='poll_detail'),
    path('polls/<int:poll_id>/results/', voting_views.poll_results, name='poll_results'),
    path('admin-panel/polls/', voting_views.admin_polls, name='admin_polls'),
    path('admin-panel/polls/create/', voting_views.create_poll, name='create_poll'),
    path('admin-panel/polls/<int:poll_id>/edit/', voting_views.edit_poll, name='edit_poll'),
    path('admin-panel/polls/<int:poll_id>/delete/', voting_views.delete_poll, name='delete_poll'),
    path('admin-panel/polls/<int:poll_id>/choices/<int:choice_id>/delete/',voting_views.delete_choice,name='delete_choice'),
    path("advertisement/delete/<int:id>/", views.delete_advertisement, name="delete_advertisement"),
]
