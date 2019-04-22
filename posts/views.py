from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Hashtag
from .forms import PostForm,ImageForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def list(request):
    posts = Post.objects.filter(
                        Q(user__in=request.user.followings.all())
                        | Q(user = request.user.id)
                        ).order_by('-pk')
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
            # 1. 공백 단위로 쪼개서 반복문을 돌리면
            for word in post.content.split():
            # 1-1. #이 가장 앞에 있으면,
                if word.startswith('#'):
                # if word[0] == '#':
            # 1-1-1. 해시태그에 저장이 되어 있으면,
            # 1-1-2. 저장이 안되어 있으면, 만들어서 추가
                    hashtag, is_created = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag)
                    # 만들어지면 : (hashtag object, True)
                    # 가져와지면 : (hashtag object, False)
            
            return redirect(post)
            # return redirect('posts:detail', post.pk)
    else:        
        post_form = PostForm()
        image_form = ImageForm()
    context = {'post_form': post_form, 'image_form': image_form}
    return render(request, 'posts/forms.html', context)
    
def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comment_set.all()
    return render(request, 'posts/detail.html', {'post': post, 'comments':comments})
    
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
        
@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    hashtag, is_created = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(hashtag)
            return redirect(post)
    else:        
        post_form = PostForm(instance=post)
    context = {'post_form': post_form}
    return render(request, 'posts/forms.html', context)
    

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

def comments_create(request, post_pk):
    if request.method == 'POST':
        print('갓냐')
        post = Post.objects.get(pk=post_pk)
        comment = Comment()
        comment.content = request.POST.get('content')
        comment.post = post
        comment.user = request.user
        comment.save()
        comments = post.comment_set.all()
        print(comments)
        return redirect('posts:detail', post.pk, {'comments':comments})

def comments_delete(request, post_pk, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
    
    return redirect('posts:detail', post_pk)

def hashtag(request, hashtag_pk):
    # 해시태그 해당하는 pk 가져와서,
    hashtag = Hashtag.objects.get(pk=hashtag_pk)
    print(hashtag)
    print('asd')
    # 템플릿에서 출력 : 해당 해시태그가 있는 글들 - 제목만
    posts = hashtag.posts.all()
    print(posts)
    context = {'posts':posts, 'hashtag':hashtag}
    return render(request, 'posts/hashtag.html', context)