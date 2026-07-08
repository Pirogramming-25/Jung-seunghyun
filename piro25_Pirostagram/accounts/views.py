from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .models import User, Follow


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # 가입 후 바로 로그인
            return redirect('posts:feed')  # 메인 피드로
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('posts:feed')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username) #팔로우 대상
    if target != request.user:
        #이미 팔로우 중인지 찾기
        follow, created = Follow.objects.get_or_create(
            from_user = request.user, to_user=target
        )
        if not created:
            follow.delete()
    return redirect('accounts:profile', username=username)

#프로필 페이지(유저 피드 페이지)
@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()   # 그 유저의 게시글들

    # 내가 이 사람을 팔로우 중인지
    is_following = Follow.objects.filter(
        from_user=request.user, to_user=profile_user
    ).exists()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    })