from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Department(models.Model):
    name = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    profile_text = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('factory', '工場への提案'),
        ('administration', '一般管理部門への提案'),
        ('regulations', '規則への提案'),
        ('technology', '技術本部への提案'),
        ('sales', '営業への提案'),
    )
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    @property
    def classname(self):
        return self.name

    def __str__(self):
        return self.get_name_display()

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 追加
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def num_likes(self):
        return self.like_set.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # 追加
