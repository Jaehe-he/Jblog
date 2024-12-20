from django.shortcuts import render, redirect
from django.utils import timezone
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm  # 카테고리 폼을 가져와야 함
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm  # 필요한 폼을 가져옵니다.
from .forms import PostForm
from .models import Post, Category
from django.shortcuts import render, redirect
# 로그인 뷰
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

# 홈 뷰 (처음 접속 시 로그인 페이지로 리디렉션)
def home(request):
    if request.user.is_authenticated:
        return redirect('post_list')  # 로그인한 경우 게시글 목록 페이지로 리디렉션
    else:
        return redirect('login')  # 로그인하지 않은 경우 로그인 페이지로 리디렉션


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')  # 로그인 후 post_list 페이지로 리디렉션
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# 로그아웃 뷰
def logout_view(request):
    logout(request)
    return redirect('home')  # 로그아웃 후 홈 페이지로 리디렉션

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'There was an error creating your account.')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})
 # Post 모델을 가져와야 합니다

# 게시글 목록 뷰
def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    user_profile = request.user.profile
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'user_profile' : user_profile})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    categories = Category.objects.all()  # 모든 카테고리 가져오기
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category_id = request.POST.get('category')  # 선택한 카테고리 설정
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'categories': categories})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()  # 모든 카테고리 가져오기
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.category_id = request.POST.get('category')  # 선택한 카테고리 설정
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'categories': categories, 'post': post})

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)  # 해당 카테고리의 게시물 가져오기
    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category})

def category_list(request):
    categories = Category.objects.all()  # 모든 카테고리 가져오기
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # 카테고리 추가
            return redirect('category_list')  # 카테고리 목록으로 리디렉션
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  # 카테고리 수정
            return redirect('category_list')  # 카테고리 목록으로 리디렉션
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_form.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'blog/profile.html', {'user_profile': profile})


def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 수정 후 프로필 페이지로 리디렉션
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'form': form})


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile  # Profile 모델을 가져옵니다.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile

def blog_posts(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None  # 프로필이 없으면 None으로 처리
    return render(request, 'blog/posts.html', {'profile': profile})