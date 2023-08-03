from django import forms
from .models import Suggestion, Category, Profile, Message  # Message を追加

class MessageForm(forms.ModelForm):  # 新しい MessageForm クラス
    class Meta:
        model = Message
        fields = ['content']  # sender と recipient はビューで設定します

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = [
            'content',
            'category',
            'business_details',
            'business_start_date',
            'fixed_asset_investment_year1',
            'non_fixed_asset_investment_year1',
            'depreciation_year1',
            'other_expenses_year1',
            'revenue_year1',
            'fixed_asset_investment_year2',
            'non_fixed_asset_investment_year2',
            'depreciation_year2',
            'other_expenses_year2',
            'revenue_year2',
            'fixed_asset_investment_year3',
            'non_fixed_asset_investment_year3',
            'depreciation_year3',
            'other_expenses_year3',
            'revenue_year3',
            'disposal_amount',
            'yield_rate',
        ]

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'skills', 'profile_text', 'profile_picture']
