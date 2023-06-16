from django import forms
from .models import Suggestion, Category

class SuggestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Suggestion
        fields = ['content', 'category']
