from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('create/', views.create_poll, name='create_poll'),
    path('<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('<int:poll_id>/choices/add/', views.add_choice, name='add_choice'),
    path('<int:poll_id>/choices/<int:choice_id>/delete/', views.delete_choice, name='delete_choice'),
    path('<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
]
