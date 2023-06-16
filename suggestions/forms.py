from django import forms
from .models import Suggestion, Category,Profile

class SuggestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Suggestion
        fields = ['content', 'category']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'skills', 'profile_text', 'profile_picture']
