from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from poems.models import Poem
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreatePoemForm, CreateReviewPoemForm
from django.contrib.auth.decorators import login_required


def home(request):
    poems = Poem.objects.all()
    user = request.user

    paginator = Paginator(poems, 3)
    page_number = request.GET.get('page')
    poem_paginated = paginator.get_page(page_number)

    context = {
        "poems": poem_paginated,
        "user": user,
    }
    return render(request, "poems/home.html", context)


@login_required(login_url="poems:home")
def poem_create(request):
    if request.method == "POST":
        form = CreatePoemForm(request.POST)
        if form.is_valid():
            poem = form.save()
            username = request.POST.get('author', None)
            author = get_object_or_404(User, username=username)
            poem.author = author
            poem.save()

    form = CreatePoemForm()
    context = {
        "form": form
    }

    return render(request, "poems/create_poem.html", context)


def poem_detail(request, pk):
    user = request.user

    if request.method == "POST" and user.is_authenticated:
        form = CreateReviewPoemForm(request.POST)
        if form.is_valid():
            review = form.save()
            username = request.POST.get('author_id', None)
            author = get_object_or_404(User, username=username)
            poem = get_object_or_404(Poem, pk=pk)
            review.author_id = author
            review.poem.add(poem)
            review.save()
    if request.method == "POST" and not user.is_authenticated:
        messages.error(
            request,
            'User must be authorized'
        )
    poem = get_object_or_404(Poem, pk=int(pk))
    reviews = poem.review.all()

    context = {
        'poem': poem,
        "reviews": reviews
    }
    return render(request, 'poems/poem.html', context)
