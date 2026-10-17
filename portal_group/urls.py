from django.urls import include, path
from portal_group import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', views.MainView.as_view(), name='main'),
     path('register/', views.register, name='register'),
     path('register_as_user/', views.register_as_user, name='register_as_user'),
     path('login/', views.login_view, name='login'),
     path('profile/', views.profile, name='profile'),
     path('admin-panel/', views.admin_panel, name='admin_panel'),
     path('admin-panel/users/', views.admin_users, name='admin_users'),
     path('profile/edit/', views.edit_profile, name='edit_profile'),
     path('logout/', views.logout_view, name='logout'),
     path('admin-panel/users/<int:user_id>/edit/',
         views.admin_edit_user, name='admin_edit_user'),
     path('admin-panel/users/<int:user_id>/delete/',
         views.admin_delete_user, name='admin_delete_user'),
     path('forum/', views.forum, name='topic_list'),
     path('events/', views.event_calendar, name='event_calendar'),
     path('events/create/', views.event_create, name='event_create'),
     path('events/<int:event_id>/', views.event_detail, name='event_detail'),
     path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
     path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
     path('advertisement/', views.advertisement, name='advertisement'),
     path('advertisement/create/', views.create_advertisement,
         name='create_advertisement'),
     path('polls/', include('voting.urls')),
     path("advertisement/delete/<int:id>/",
         views.delete_advertisement, name="delete_advertisement"),
     path('gallery/', views.gallery, name='gallery'),
     path('gallery/create/', views.gallery_create, name='gallery_create'),
     path('gallery/<int:image_id>/delete/', views.gallery_delete, name='gallery_delete'),
     path('portfolio/', views.portfolio, name='portfolio'),
     path('portfolio/create/', views.portfolio_create, name='portfolio_create'),
     path('portfolio/<int:pk>/edit/', views.portfolio_edit, name='portfolio_edit'),
     path('portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
