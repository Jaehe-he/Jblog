from django.contrib import admin
from .models import Post, Category, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'gender', 'bio')  # 표시할 필드 설정
    search_fields = ('user__username',)

admin.site.register(Post)
admin.site.register(Category)