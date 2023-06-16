from django.db import models

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
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
