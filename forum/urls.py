from django.urls import path
from forum import views


urlpatterns = [
    path(
        "topic_list/",
        views.topic_list,
        name="topic_list",
    ),

    path(
        "create_category/",
        views.create_category,
        name="create_category",
    ),

    path(
        "category/<int:category_id>/",
        views.category_detail,
        name="category_detail",
    ),

    path(
        "category/<int:category_id>/create_topic/",
        views.create_topic,
        name="create_topic_in_category",
    ),

    path(
        "topic/<int:topic_id>/",
        views.topic_detail,
        name="topic_detail",
    ),

    path(
        "create_topic/",
        views.create_topic,
        name="create_topic",
    ),

    path(
        "category/<int:category_id>/delete/",
        views.delete_category,
        name="delete_category",
),
]