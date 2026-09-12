from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .models import Advertisement
from .forms import ProfileForm, RegisterForm


class MainView(TemplateView):
    template_name = "portal_group/main.html"


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
    else:
        form = RegisterForm()

    return render(request, "portal_group/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profile")

        return render(request, "portal_group/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "portal_group/login.html")


@login_required
def profile(request):
    return render(request, "portal_group/profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "portal_group/edit_profile.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("main")

# Advertisement


@login_required
def create_advertisement(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")

        if title and text:
            Advertisement.objects.create(
                title=title,
                text=text,
                creator=request.user
            )
            return redirect("advertisement")

    return render(request, "portal_group/create_advertisement.html")


def advertisement(request):
    advertisements = Advertisement.objects.all().order_by("-created_at")
    return render(request, "portal_group/advertisement.html", {"advertisements": advertisements})
