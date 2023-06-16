from django.urls import path
from suggestions.views import index, suggestion_list, suggestion_create, suggestion_detail, profile, edit_profile
from django.contrib import admin
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='suggestions/login.html'), name='login'),
    path('', index, name='index'),
    path('create/', suggestion_create, name='suggestion_create'),
    path('list/', suggestion_list, name='suggestion_list'),
    path("admin/",admin.site.urls),
    path('suggestion/<int:suggestion_id>/', suggestion_detail, name='suggestion_detail'),
    path('profile/', profile, name='profile'), # 既存のビューを名前付きURLパターンとして追加
    path('profile/edit/', edit_profile, name='edit_profile'),
]
