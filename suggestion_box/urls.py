from django.urls import path
from suggestions.views import suggestion_list, suggestion_create
from django.contrib import admin


urlpatterns = [
    path('', suggestion_create, name='suggestion_create'),
    path('list/', suggestion_list, name='suggestion_list'),
    path("admin/",admin.site.urls),
]
