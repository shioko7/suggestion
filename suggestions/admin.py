from django.contrib import admin
from .models import Department, Profile, Category, Suggestion, Like, Message

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'skills', 'profile_text']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at', 'category']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'suggestion', 'created_at']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'content', 'created_at', 'is_read']

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Message, MessageAdmin)
