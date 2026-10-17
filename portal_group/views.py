from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from .models import Advertisement, GalleryImage
from .forms import ProfileForm, RegisterForm, AdminUserForm, RegisterForm2


class MainView(TemplateView):
    template_name = "portal_group/main.html"


# Authorisation
def register(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            role = form.cleaned_data['role']

            if role == 'Administrator':
                user.is_superuser = True
                user.is_staff = True
                user.save()
            else:
                match role:
                    case 'Student':
                        user.groups.add(1)
                    case 'Teacer':
                        user.groups.add(2)
                    case 'Administrator':
                        user.groups.add(3)

            login(request, user)

            return redirect('/')

    else:
        form = RegisterForm()

    return render(request, 'portal_group/register.html', {
        'form': form
    })


def register_as_user(request):
    if request.method == 'POST':
        form = RegisterForm2(request.POST)

        if form.is_valid():
            user = form.save()
            user.groups.add(3)

            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm2()

    return render(request, 'portal_group/register.html', {
        'form': form
    })


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


def teacher_required(view_func):
    return user_passes_test(
        lambda user: (
            user.is_authenticated
            and (
                user.groups.filter(name='Teacher').exists()
                or user.is_superuser
            )
        )
    )(view_func)


@login_required
def profile(request):
    if request.user.is_superuser:
        role = 'Administrator'
    elif request.user.groups.filter(name='Teacher').exists():
        role = 'Teacher'
    elif request.user.groups.filter(name='Student').exists():
        role = 'Student'
    else:
        role = 'Not assigned'

    return render(request, 'portal_group/profile.html', {
        'role': role
    })


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


@teacher_required
def teacher_page(request):
    return render(request, 'portal_group/teacher_page.html')


def forum(request):
    return render(request, 'topic_list.html')

# Advertisement


def advertisement_creator_required(view_func):
    # Administrators and teachers can create advertisements.
    # Students/users can only view advertisements.
    return user_passes_test(
        lambda user: (
            user.is_authenticated
            and (
                user.is_superuser
                or user.groups.filter(name='Teacher').exists()
            )
        )
    )(view_func)


@advertisement_creator_required
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

    can_create_advertisement = (
        request.user.is_authenticated
        and (
            request.user.is_superuser
            or request.user.groups.filter(name='Teacher').exists()
        )
    )

    return render(request, "portal_group/advertisement.html", {
        "advertisements": advertisements,
        "can_create_advertisement": can_create_advertisement,
    })


@login_required
def delete_advertisement(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)

    if advertisement.creator == request.user:
        advertisement.delete()

    return redirect("advertisement")


# Admin panel
@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    return render(request, 'portal_group/admin_panel.html')


@login_required
def admin_users(request):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    from django.contrib.auth.models import User, Group

    users = User.objects.all()

    for user in users:
        if user.is_superuser:
            user.role = 'Administrator'
        elif user.groups.filter(name='Teacher').exists():
            user.role = 'Teacher'
        elif user.groups.filter(name='Student').exists():
            user.role = 'Student'
        else:
            user.role = 'Not assigned'

    return render(request, 'portal_group/admin_users.html', {
        'users': users
    })


@login_required
def admin_edit_user(request, user_id):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    from django.contrib.auth.models import User, Group
    from .forms import AdminUserForm

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            role = form.cleaned_data['role']

            user.groups.clear()
            user.is_superuser = False
            user.is_staff = False

            if role == 'Administrator':
                user.is_superuser = True
                user.is_staff = True

            elif role == 'Teacher':
                from django.contrib.auth.models import Group
                group = Group.objects.get(name='Teacher')
                user.groups.add(group)

            elif role == 'Student':
                from django.contrib.auth.models import Group
                group = Group.objects.get(name='Student')
                user.groups.add(group)

            user.save()

            return redirect("admin_users")

    else:
        form = AdminUserForm(instance=user)

    return render(request, "portal_group/admin_edit_user.html", {
        "form": form,
        "edit_user": user
    })


@login_required
def admin_delete_user(request, user_id):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    from django.contrib.auth.models import User, Group

    user = User.objects.get(id=user_id)

    if user == request.user:
        return redirect("admin_users")

    if request.method == "POST":
        user.delete()

    return redirect("admin_users")


# School events calendar
def event_manager_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and (
            user.is_superuser or user.groups.filter(name='Teacher').exists()
        )
    )(view_func)


def event_calendar(request):
    from .models import Event
    can_manage_events = request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name='Teacher').exists()
    )
    events = Event.objects.all()
    return render(request, 'portal_group/event_calendar.html', {
        'events': events, 'can_manage_events': can_manage_events,
    })


def event_detail(request, event_id):
    from .models import Event
    event = get_object_or_404(Event, pk=event_id)
    can_manage_events = request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name='Teacher').exists()
    )
    return render(request, 'portal_group/event_detail.html', {
        'event': event, 'can_manage_events': can_manage_events,
    })


@event_manager_required
def event_create(request):
    from .models import Event
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        event_date = request.POST.get('event_date', '').strip()
        event_time = request.POST.get('event_time', '').strip() or None
        location = request.POST.get('location', '').strip()
        if title and description and event_date:
            Event.objects.create(title=title, description=description, event_date=event_date,
                                 event_time=event_time, location=location, creator=request.user)
            return redirect('event_calendar')
        return render(request, 'portal_group/event_form.html', {
            'page_title': 'Create event', 'error': 'Fill in the title, description and date.',
            'event': None, 'event_data': request.POST,
        })
    return render(request, 'portal_group/event_form.html', {'page_title': 'Create event', 'event': None})


@event_manager_required
def event_edit(request, event_id):
    from .models import Event
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        event_date = request.POST.get('event_date', '').strip()
        if title and description and event_date:
            event.title = title
            event.description = description
            event.event_date = event_date
            event.event_time = request.POST.get('event_time', '').strip() or None
            event.location = request.POST.get('location', '').strip()
            event.save()
            return redirect('event_detail', event_id=event.pk)
        return render(request, 'portal_group/event_form.html', {
            'page_title': 'Edit event', 'event': event, 'event_data': request.POST,
            'error': 'Fill in the title, description and date.',
        })
    return render(request, 'portal_group/event_form.html', {'page_title': 'Edit event', 'event': event})


@event_manager_required
def event_delete(request, event_id):
    from .models import Event
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_calendar')
    return render(request, 'portal_group/event_delete.html', {'event': event})

@login_required
def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')

    return render(request, 'portal_group/gallery.html', {
        'images': images,
    })


@login_required
def gallery_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        if title and image:
            GalleryImage.objects.create(
                title=title,
                description=description,
                image=image,
                creator=request.user,
            )
            return redirect('gallery')

    return render(request, 'portal_group/gallery_create.html')

@login_required
def gallery_delete(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)

    if request.method == 'POST':
        if request.user.is_superuser or image.creator == request.user:
            image.delete()

    return redirect('gallery')