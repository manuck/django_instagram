from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as django_logout, login as django_login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm, UserCustomCreationForm, UserCustomChangeForm
# Create your views here.

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users':users})
    
def signup(request):
    # form = UserCustomCreationForm()
    # return render(request, 'signup.html', {'form':form})
    if request.method =='POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts:profile_update')
    else:
        form = UserCustomCreationForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

def signin(request):
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = AuthenticationForm(request, request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            user = authenticate(
                username=username,
                password=password
            )
            # 인증에 성공했을 경우
            if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
                django_login(request, user)
                # Post목록 화면으로 이동
                return redirect('posts:list')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = AuthenticationForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'login.html', context)
    
@login_required
def logout(request):
    django_logout(request)
    return redirect('posts:list')

@login_required
def delete(request):
    request.user.delete()
    return redirect('posts:list')

@login_required
def update(request):
    # user_form = UserCustomChangeForm()
    if request.method == 'POST':
        user_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('boards:index')
    else:
        user_form = UserCustomChangeForm()
    context = {'user_form':user_form}
    return render(request, 'update.html', context)

def profile_update(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('posts:list')
            
    profile_form = ProfileForm(instance = request.user.profile)
    context = {'profile_form': profile_form}
    return render(request, 'profile_update.html', context)

def profile(request):
    return render(request, 'profile.html')

def detail(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    context = {'user_info': user}
    return render(request, 'detail.html', context)

def follow(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:detail', user_pk)