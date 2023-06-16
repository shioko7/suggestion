from django.urls import path
from suggestions.views import index, suggestion_list, suggestion_create,suggestion_detail
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('create/', suggestion_create, name='suggestion_create'),
    path('list/', suggestion_list, name='suggestion_list'),
    path("admin/",admin.site.urls),
    path('suggestion/<int:suggestion_id>/', suggestion_detail, name='suggestion_detail'),

]
