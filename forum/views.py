from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, PostForm, TopicForm
from .models import Category, Post, Topic


def topic_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "forum/topic_list.html",
        {
            "categories": categories,
        },
    )


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = Topic.objects.filter(category=category).order_by("-created_at")

    return render(
        request,
        "forum/category_detail.html",
        {
            "category": category,
            "topics": topics,
        },
    )


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all().order_by("created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()

            return redirect("topic_detail", topic_id=topic.id)
    else:
        form = PostForm()

    return render(
        request,
        "forum/topic_detail.html",
        {
            "topic": topic,
            "posts": posts,
            "form": form,
        },
    )


@login_required
def create_topic(request, category_id=None):
    if request.method == "POST":
        form = TopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user

            if category_id is not None:
                topic.category = get_object_or_404(
                    Category,
                    id=category_id,
                )

            topic.save()

            return redirect("topic_detail", topic_id=topic.id)
    else:
        if category_id is not None:
            form = TopicForm(
                initial={
                    "category": get_object_or_404(
                        Category,
                        id=category_id,
                    )
                }
            )
        else:
            form = TopicForm()

    return render(
        request,
        "forum/create_topic.html",
        {
            "form": form,
        },
    )


@login_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("topic_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "forum/create_category.html",
        {
            "form": form,
        },
    )

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("topic_list")

    return render(
        request,
        "forum/delete_category.html",
        {
            "category": category,
        },
    )