from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_new, name='category_new'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)