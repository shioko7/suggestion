from django.urls import path
from suggestions import views
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='suggestions/login.html'), name='login'),
    path('', views.index, name='index'),
    path('create/', views.suggestion_create, name='suggestion_create'),
    path('list/', views.suggestion_list, name='suggestion_list'),
    path("admin/",admin.site.urls),
    path('suggestion/<int:suggestion_id>/', views.suggestion_detail, name='suggestion_detail'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('suggestions/<int:suggestion_id>/edit/', views.suggestion_edit, name='suggestion_edit'),
    path('suggestions/<int:suggestion_id>/delete/', views.suggestion_delete, name='suggestion_delete'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/new/<int:recipient_id>/', views.message_create, name='message_create'),
    path('like_suggestion/', views.like_suggestion, name='like_suggestion'),  # like_suggestionビューへのURLを追加




]
