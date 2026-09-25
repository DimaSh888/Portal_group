from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .models import Poll


def poll_manager_required(view_func):
    """Only administrators and teachers can manage polls."""
    return user_passes_test(
        lambda user: (
            user.is_authenticated
            and (
                user.is_superuser
                or user.groups.filter(name='Teacher').exists()
            )
        )
    )(view_func)


def can_manage_polls(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name='Teacher').exists()
        )
    )


@login_required
def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')

    return render(request, 'voting/poll_list.html', {
        'polls': polls,
        'can_manage_polls': can_manage_polls(request.user),
    })


@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    already_voted = poll.choices.filter(votes=request.user).exists()

    if request.method == 'POST':
        if already_voted:
            return redirect('poll_results', poll_id=poll.id)

        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(poll.choices, id=choice_id)
            choice.votes.add(request.user)
            return redirect('poll_results', poll_id=poll.id)

    return render(request, 'voting/poll_detail.html', {
        'poll': poll,
        'already_voted': already_voted,
    })


@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = poll.choices.all()
    total_votes = sum(choice.votes.count() for choice in choices)

    results = []
    for choice in choices:
        votes = choice.votes.count()
        percentage = round(votes / total_votes * 100, 1) if total_votes else 0
        results.append({
            'text': choice.text,
            'votes': votes,
            'percentage': percentage,
        })

    return render(request, 'voting/poll_results.html', {
        'poll': poll,
        'total_votes': total_votes,
        'results': results,
        'can_manage_polls': can_manage_polls(request.user),
    })


@poll_manager_required
def create_poll(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            poll = Poll.objects.create(title=title, description=description)
            return redirect('add_choice', poll_id=poll.id)

    return render(request, 'voting/create_poll.html')


@poll_manager_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            poll.title = title
            poll.description = description
            poll.save()
            return redirect('poll_list')

    return render(request, 'voting/edit_poll.html', {'poll': poll})


@poll_manager_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            poll.choices.create(text=text)
            return redirect('add_choice', poll_id=poll.id)

    return render(request, 'voting/add_choice.html', {
        'poll': poll,
        'choices': poll.choices.all(),
    })


@poll_manager_required
def delete_choice(request, poll_id, choice_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choice = get_object_or_404(poll.choices, id=choice_id)

    if request.method == 'POST':
        choice.delete()
        return redirect('add_choice', poll_id=poll.id)

    return render(request, 'voting/delete_choice.html', {
        'poll': poll,
        'choice': choice,
    })


@poll_manager_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == 'POST':
        poll.delete()
        return redirect('poll_list')

    return render(request, 'voting/delete_poll.html', {'poll': poll})
