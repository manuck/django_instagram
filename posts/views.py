from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm,ImageForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
    
@login_required
def new(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            files = request.FILES.getlist('file')
            for file in files:
                request.FILES['file'] = file
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect(post)
            # return redirect('posts:detail', post.pk)
    else:        
        post_form = PostForm()
        image_form = ImageForm()
    context = {'post_form': post_form, 'image_form': image_form}
    return render(request, 'posts/forms.html', context)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    return render(request, 'posts/detail.html', {'post': post})
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            post.delete()
            return redirect('posts:list')
        else:
            return redirect(post)
    else:
        return redirect('posts:list')
        
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=post)
            if post_form.is_valid():
                post = post_form.save()
                return redirect(post)
        else:
            post_form = PostForm(instance=post)
        context = {'post_form': post_form}
        return render(request, 'posts/forms.html', context)
    else:
        return redirect('posts:list')
    

def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    # user가 지금 해당 게시글에 좋아요를 한적이 있는지?
    # if user in post.like_users.all():
    #     post.like_users.remove(user)
    # else:
    #     post.like_users.add(user)
    if post.like_users.filter(pk=user.id).exists():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
        
    return redirect('posts:detail', post_pk)