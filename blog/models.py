from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profiles_pics/')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')  # 성별 필드 추가
    bio = models.TextField(blank=True)  # 한 줄 소개 필드 추가

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)  # 명시적으로 기본 키 정의
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank = True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # 카테고리 추가

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

