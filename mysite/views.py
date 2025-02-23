from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'blog/index.html')


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blog/detail.html', context)


def tickets(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(description=cd['description'], name=cd['name'], last_name=cd['last_name'],
                                         email=cd['email'], phone=cd['phone'], subject=cd['subject'])
            return redirect('mysite:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }

    return render(request, 'forms/comment.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            return redirect('mysite:profile')
    else:
        form = PostForm()
    return render(request, 'forms/create-post.html', {'form': form})


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.published.annotate(trigram=TrigramSimilarity('title', query) +
                                              TrigramSimilarity('description', query)).\
                filter(trigram__gte=0.1)
            images = Image.objects.annotate(trigram=TrigramSimilarity('title', query) +
                                              TrigramSimilarity('description', query)).\
                filter(trigram__gte=0.1)
            result = list(posts) + list(images)

            results = sorted(result, key=lambda x: x.trigram, reverse=True)
        context = {
            'query': query,
            'results': results,
            }
        return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    paginator = Paginator(posts, 2)
    page_obj = request.GET.get('page')
    try:
        posts = paginator.page(page_obj)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/profile.html', context)

# @login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            return redirect('mysite:profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('mysite:profile')
    return render(request, 'forms/delete_post.html', {'post': post})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('mysite:profile')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('mysite:profile')
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('You are not logged in.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def log_out(request):
    logout(request)
    return render(request,  'registration/logged_out.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register-done.html', {'user': user})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_account(request):
    if request.method == "POST":
        user = UserEditForm(request.POST, instance=request.user)
        account = AccountEditForm(request.POST, files=request.FILES, instance=request.user.account)
        if user.is_valid() and account.is_valid():
            user.save()
            account.save()
            return redirect('mysite:profile')
    else:
        user = UserEditForm(instance=request.user)
        account = AccountEditForm(instance=request.user.account)
    context = {
        'user': user,
        'account': account,
    }
    return render(request, 'registration/edit_account.html', context)







