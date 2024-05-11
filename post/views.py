from django.shortcuts import render, redirect
from django.http import Http404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post, Doc, Tag
from main.models import Profile
from .NLP import preprocess, topic_ide, create_dictionary, cosin_sim_ide
from django.urls import reverse
import json

# Create your views here.

def doc_create(text, post):
    doc = Doc()
    doc.post = post
    doc.processed_text = json.dumps(text)
    return doc

@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.save()
            post = Post.objects.last()
            texts = preprocess(post.file)
            dic = create_dictionary(texts)
            doc = doc_create(texts, post)
            doc.save()
            tags = topic_ide(texts, dic)
            existing_tags = Tag.objects.filter(name__in=tags)
            existing_tag_names = set(tag.name for tag in existing_tags)
            new_tags = [tag for tag in tags if tag not in existing_tag_names]
            for new_tag in new_tags:
                tag = Tag(name=new_tag)
                tag.save()
            add_tags = Tag.objects.filter(name__in=tags)
            for tag in add_tags:
                tag.post.add(post)    
            return redirect('home')
        else:
            return render(request, 'post/create_post.html', {"form": form})
    else:
        form = PostForm()
        return render(request, 'post/create_post.html', {"form": form})

@login_required(login_url="/login")
def view_post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        raise Http404('post not found')
    tags = Tag.objects.filter(post__id = post_id)
    profile = Profile.objects.get(user__id = post.author.pk)
    tag_posts = Post.objects.filter(tag__in=tags)
    similar_posts = []
    for tag_post in tag_posts:
        common_tags = tag_post.tag_set.filter(id__in=tags)
        if len(common_tags) >= 2 and tag_post != post and tag_post not in similar_posts:
            similar_posts.append(tag_post)
    context = {'post': post, 'tags':tags, 'profile':profile, 'similar_posts':similar_posts}
    return render(request, 'post/view_post.html', context)

@login_required(login_url="/login")
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        raise Http404('post not found')
    if request.user != post.author:
        return redirect('home')
    post.tag_set.clear()
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            texts = preprocess(post.file)
            dic = create_dictionary(texts)
            existed_doc = True
            try:
                doc = Doc.objects.get(post__id = post.pk)
            except Doc.DoesNotExist:
                doc = doc_create(texts, post)
                doc.save()
                existed_doc = False
            if existed_doc: 
                doc.processed_text = json.dumps(texts)
                doc.save()
            tags = topic_ide(texts, dic)
            existing_tags = Tag.objects.filter(name__in=tags)
            existing_tag_names = set(tag.name for tag in existing_tags)
            new_tags = [tag for tag in tags if tag not in existing_tag_names]
            for new_tag in new_tags:
                tag = Tag(name=new_tag)
                tag.save()
            add_tags = Tag.objects.filter(name__in=tags)
            for tag in add_tags:
                tag.post.add(post)  
            return redirect(reverse('view_post', args=[post_id]))
        else:
            return render(request, 'post/edit_post.html', {'post_form':post_form})
    else:
        post_form = PostForm(instance=post)
    return render(request, 'post/edit_post.html', {'post_form':post_form})

@login_required(login_url='/login')
def delete(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return redirect(reverse('home'))
    user = request.user
    if user == post.author:
        post.delete()
        return redirect(reverse('profile', args=[user.pk]))
    else:
        return redirect(reverse('home'))

@login_required(login_url='/login')
def compare(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        id1 = request.POST.get('post1')
        id2 = request.POST.get('post2')
        if id1 and id2:
            post1 = Post.objects.filter(id = id1).first() or None
            post2 = Post.objects.filter(id = id2).first() or None
            if post1 and post2:
                try:
                    doc1 = Doc.objects.get(post__id = id1)
                except Doc.DoesNotExist:
                    doc1 = doc_create(preprocess(post1.file), post1)
                    doc1.save()
                try:
                    doc2 = Doc.objects.get(post__id = id2)
                except Doc.DoesNotExist:
                    doc2 = doc_create(preprocess(post2.file), post2)
                    doc2.save()
                text1 = json.loads(doc1.processed_text)
                text2 = json.loads(doc2.processed_text)
                similarity = cosin_sim_ide(text1, text2)
                context = {'post1':post1, 'post2':post2, 'posts':posts, 'post1':post1, 'post2':post2, 'similarity':similarity}
                return render(request, 'post/compare.html', context)
        else:
            return render(request, 'post/compare.html', {'posts':posts})
    return render(request, 'post/compare.html', {'posts':posts})