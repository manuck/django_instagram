from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
    
def new(request):
    post = Post()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'posts/forms.html', context)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    return render(request, 'posts/detail.html', {'post': post})
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')
    else:
        return redirect(post)
        
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/forms.html', context)
    