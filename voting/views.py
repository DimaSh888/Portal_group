from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Poll


def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')

    return render(request, 'voting/poll_list.html', {
        'polls': polls
    })

@login_required
def poll_detail(request, poll_id):
    poll = Poll.objects.get(id=poll_id)

    already_voted = poll.choices.filter(votes=request.user).exists()

    if request.method == 'POST':

        if already_voted:
            return redirect('poll_results', poll_id=poll.id)

        choice_id = request.POST.get('choice')

        if choice_id:
            choice = poll.choices.get(id=choice_id)
            choice.votes.add(request.user)

            return redirect('poll_results', poll_id=poll.id)

    return render(request, 'voting/poll_detail.html', {
        'poll': poll
    })

def poll_results(request, poll_id):
    poll = Poll.objects.get(id=poll_id)

    choices = poll.choices.all()

    total_votes = sum(
        choice.votes.count()
        for choice in choices
    )

    results = []

    for choice in choices:
        votes = choice.votes.count()

        if total_votes > 0:
            percentage = round(votes / total_votes * 100, 1)
        else:
            percentage = 0

        results.append({
            'text': choice.text,
            'votes': votes,
            'percentage': percentage
        })

    return render(request, 'voting/poll_results.html', {
        'poll': poll,
        'total_votes': total_votes,
        'results': results
    })

@login_required
def admin_polls(request):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    polls = Poll.objects.all().order_by('-created_at')

    return render(request, 'voting/admin_polls.html', {
        'polls': polls
    })

@login_required
def create_poll(request):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title:
            Poll.objects.create(
                title=title,
                description=description
            )

            return redirect('admin_polls')

    return render(request, 'voting/create_poll.html')

@login_required
def edit_poll(request, poll_id):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    poll = Poll.objects.get(id=poll_id)

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            poll.choices.create(text=text)

            return redirect('edit_poll', poll_id=poll.id)

    return render(request, 'voting/edit_poll.html', {
        'poll': poll
    })

@login_required
def delete_poll(request, poll_id):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    poll = Poll.objects.get(id=poll_id)

    if request.method == 'POST':
        poll.delete()
        return redirect('admin_polls')

    return render(request, 'voting/delete_poll.html', {
        'poll': poll
    })

@login_required
def delete_choice(request, poll_id, choice_id):
    if not request.user.is_superuser:
        return render(request, 'portal_group/register_denied.html')

    poll = Poll.objects.get(id=poll_id)
    choice = poll.choices.get(id=choice_id)

    if request.method == 'POST':
        choice.delete()
        return redirect('edit_poll', poll_id=poll.id)

    return render(request, 'voting/delete_choice.html', {
        'poll': poll,
        'choice': choice
    })