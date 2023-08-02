from django import forms
from .models import Suggestion, Category, Profile, Message  # Message を追加

class MessageForm(forms.ModelForm):  # 新しい MessageForm クラス
    class Meta:
        model = Message
        fields = ['content']  # sender と recipient はビューで設定します

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['content', 'category', 'cost', 'expected_revenue'] # コストと期待収益のフィールドを追加


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'skills', 'profile_text', 'profile_picture']
