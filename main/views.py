from django.shortcuts import render, redirect
from django.http import Http404
from .forms import signup_form, user_edit_form, profile_edit_form
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile, User
from post.models import Post, Tag
from django.db.models import Q, Count
# Create your views here.

@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all().order_by('-updated')
    tags = Tag.objects.all()
    popular_tags = Tag.objects.annotate(post_count=Count('post')).order_by('-post_count')[:10]
    context = {'posts':posts, 'tags':tags, 'popular_tags':popular_tags}
    return render(request, 'main/home.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile()
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = signup_form()
    return render(request, "registration/signup.html", {'form':form})

@login_required(login_url='/login')
def profile(request, user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404('user not found')
    if Profile.objects.filter(user__id=user_id).exists():
        profile = Profile.objects.get(user__id=user_id)
    else:
        profile = Profile()
        profile.user = user
        profile.save()
    posts = Post.objects.filter(author__id=user_id)
    post_num = len(posts)
    tags = Tag.objects.all()
    context = {'current_user':user, 'profile':profile, 'posts':posts, 'post_num':post_num, 'tags':tags}
    return render(request, "main/profile.html", context)

@login_required(login_url='/login')
def profile_edit(request):
    user = request.user
    if Profile.objects.filter(user__id=user.pk).exists():
        profile = Profile.objects.get(user__id=user.pk)
    else:
        profile = Profile()
        profile.user = user
        profile.save()
    if request.method == 'POST':
        user_form = user_edit_form(request.POST, instance=user)
        profile_form = profile_edit_form(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile/' + str(user.pk))
        else:
            context = {'user_form':user_form, 'profile_form':profile_form}
            return render(request, "main/profile_edit.html", context)
    else:
        profile_form = profile_edit_form(instance=profile)
        user_form = user_edit_form(instance=user)
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, "main/profile_edit.html", context)

@login_required(login_url='/login')
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        words = searched.split()
        posts = []
        for word in words:
            search_posts = Post.objects.filter(Q(title__contains=word) | Q(author__username__contains=word) | Q(tag__name__contains=word))
            for search_post in search_posts:
                if search_post not in posts:
                    posts.append(search_post)
        return render(request, 'main/search.html', {'searched':searched, 'posts':posts})
    return render(request, "main/search.html")

