from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Follow
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm, FilterForm
from django.contrib.auth.decorators import login_required
from .utils import paginator
from django.urls import reverse

from django.views.generic import ListView
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    # 
    if request.method == 'POST':
        post_filter = PostFilter(request.POST, queryset=post_list)
    else:
        post_filter = PostFilter(queryset=post_list)
    # page_obj = paginator(request, post_list)
    page_obj = Paginator(post_filter.qs, 5).get_page(request.GET.get('page'))
    context = {
        'title': 'Последние обновления на сайте',
        'posts': post_filter,
        'page_obj': page_obj,
    }
    return render(request, template, context)


class PostListView(FilterView):
    model = Post
    filterset_class = PostFilter
    paginate_by = 10
    template_name = 'posts/filter.html'

# def filter_index(request):
#     template = 'posts/index.html'
#     form = FilterForm()

#     post_list = Post.objects.all()
#     page_obj = paginator(request, post_list)
#     context = {
#         'title': 'Последние обновления на сайте',
#         'posts': post_list,
#         'page_obj': page_obj,
#         'form': form
#     }

#     return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginator(request, post_list)
    context = {
        'group': group,
        'posts': post_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'

    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    page_obj = paginator(request, post_list)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author=user,
        ).exists()
    else:
        following = False
    profile = user
    context = {
        'author': user,
        'page_obj': page_obj,
        'following': following,
        'profile': profile
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'

    form = CommentForm()
    post = get_object_or_404(Post, id=post_id)

    comments = post.comments.all()
    posts_count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'posts_count': posts_count,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'

    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'

    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator(request, post_list)
    context = {
        'title': 'Последние обновления на сайте',
        'posts': post_list,
        'page_obj': page_obj,
    }

    return render(request, template, context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(user=user, author=author)
    if user != author and not followers.exists():
        Follow.objects.create(user=user, author=author)
    return redirect(reverse('posts:profile', kwargs={'username': username}))


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(user=request.user, author=author)
    if followers.exists():
        followers.delete()
    return redirect(reverse('posts:profile', kwargs={'username': author}))
