from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Suggestion, Like ,Message,Profile # Like を追加
from .forms import SuggestionForm, EditProfileForm, MessageForm # UserProfileFormとMessageFormを追加
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # JsonResponseを追加
from django.views.decorators.http import require_POST  # require_POSTを追加
from django.contrib.auth.models import User  # Userモデルのインポートを追加
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncDay,TruncMonth
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.db.models.functions import TruncWeek
from django_pandas.io import read_frame
import pandas as pd
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Department

def department_members(request, department_id):
    department = Department.objects.get(id=department_id)
    team_members = department.profile_set.all()
    departments = Department.objects.all()
    return render(request, 'team_members.html', {'team_members': team_members, 'department_name': department.name, 'departments': departments})


def get_suggestion_ranking():
    return Suggestion.objects.annotate(like_count=Count('like')).order_by('-like_count')

def get_user_ranking():
    return User.objects.annotate(suggestion_count=Count('suggestion')).order_by('-suggestion_count')




@login_required
def profile(request):
    return render(request, 'suggestions/edit_profile.html')



def index(request):
    return render(request, 'suggestions/index.html')


@login_required
def suggestion_list(request, year, month):
    year = int(year)
    month = int(month)

    # 前月と次月を計算
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    # 指定された年と月の範囲で提案をフィルタリング
# 指定された年の範囲で提案をフィルタリング
    start_date = timezone.make_aware(timezone.datetime(year=year, month=1, day=1))
    end_date = timezone.make_aware(timezone.datetime(year=year + 1, month=1, day=1))

    suggestions = Suggestion.objects.filter(created_at__range=(start_date, end_date)).order_by('-created_at')


    suggestion_ranking = get_suggestion_ranking()
    user_ranking = get_user_ranking()
    user_likes = Like.objects.filter(user=request.user).values_list('suggestion_id', flat=True)

    context = {
        'suggestions': suggestions,
        'suggestion_ranking': suggestion_ranking,
        'user_ranking': user_ranking,
        'user_likes': user_likes,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'now_year': year,
        'now_month': month,
    }

    return render(request, 'suggestions/list.html', context)


@login_required
@require_POST
def like_suggestion(request):
    suggestion_id = request.POST.get('post_pk')
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    like = Like.objects.filter(suggestion=suggestion, user=request.user)
    context = {}
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        Like.objects.create(suggestion=suggestion, user=request.user)
        context['method'] = 'create'
    context['like_count'] = Like.objects.filter(suggestion=suggestion).count()
    return JsonResponse(context)


@login_required
def suggestion_detail(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)


    yield_rate = float(suggestion.yield_rate) / 100# 1年目、2年目、3年目の投資額①を計算
    investment_amounts = [
        float(suggestion.fixed_asset_investment_year1) + float(suggestion.non_fixed_asset_investment_year1),
        float(suggestion.fixed_asset_investment_year2) + float(suggestion.non_fixed_asset_investment_year2),
        float(suggestion.fixed_asset_investment_year3) + float(suggestion.non_fixed_asset_investment_year3),
        ]

# 1年目、2年目、3年目のCFを計算
    cf_values = [
        (float(suggestion.revenue_year1) - float(suggestion.depreciation_year1) - float(suggestion.other_expenses_year1)) * 0.6 + float(suggestion.depreciation_year1),
        (float(suggestion.revenue_year2) - float(suggestion.depreciation_year2) - float(suggestion.other_expenses_year2)) * 0.6 + float(suggestion.depreciation_year2),
        (float(suggestion.revenue_year3) - float(suggestion.depreciation_year3) - float(suggestion.other_expenses_year3)) * 0.6 + float(suggestion.depreciation_year3),
        ]

#

# 1年目、2年目、3年目のPVを計算
    pv_values = [
        (cf_values[0] + float(suggestion.disposal_amount) - investment_amounts[0]) * (1 / (1 + yield_rate)),
        (cf_values[1] + float(suggestion.disposal_amount) - investment_amounts[1]) * (1 / ((1 + yield_rate) ** 2)),
        (cf_values[2] + float(suggestion.disposal_amount) - investment_amounts[2]) * (1 / ((1 + yield_rate) ** 3)),
        ]

    # NPVを計算
    npv = sum(pv_values)

    # 現価係数
    discount_factors = [1 / (1 + yield_rate) ** i for i in range(1, 4)]

    context = {
        'suggestion': suggestion,
        'investment_amounts': investment_amounts,
        'cf_values': cf_values,
        'discount_factors': discount_factors,
        'pv_values': pv_values,
        'npv': npv,
    }

    return render(request, 'suggestions/suggestion_detail.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:
        return redirect('login')


@login_required
def suggestion_create(request):
    now = datetime.now()
    now_year = now.year
    now_month = now.month
    categories = Category.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            return redirect('suggestion_list', year=now_year, month=now_month)
    else:
        form = SuggestionForm()
    return render(request, 'suggestions/create.html', {'form': form, 'categories': categories})




@login_required
def suggestion_edit(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    if request.method == 'POST':
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('suggestion_detail', suggestion_id=suggestion.id)
    else:
        form = SuggestionForm(instance=suggestion)
    return render(request, 'suggestions/suggestion_edit.html', {'form': form, 'suggestion': suggestion})

@login_required
def suggestion_delete(request, suggestion_id):
    now = datetime.now()
    now_year = now.year
    now_month = now.month
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    if request.method == 'POST':
        suggestion.delete()
        return redirect('suggestion_list', year=now_year ,month=now_month)
    return render(request, 'suggestions/suggestion_delete.html', {'suggestion': suggestion})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'suggestions/edit_profile.html', {'form': form, 'member': request.user})


@login_required
def message_create(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'suggestions/message_create.html', {'form': form, 'recipient': recipient})


@login_required
def message_list(request):
    messages = Message.objects.filter(recipient=request.user)
    recipient_id = request.user.id
    return render(request, 'suggestions/message_list.html', {'messages': messages, 'recipient_id': recipient_id})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user:
        raise Http404
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'suggestions/message_detail.html', {'message': message})



@login_required
def message_thread(request, sender_id, recipient_id):
    sender = get_object_or_404(User, id=sender_id)
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
    else:
        form = MessageForm()
    messages = Message.objects.filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender))
    return render(request, 'suggestions/message_thread.html', {'form': form, 'messages': messages})



class MonthDashboard(LoginRequiredMixin, generic.TemplateView):
    """月間提案ダッシュボード"""
    template_name = 'suggestions/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['now_year'] = year
        context['now_month'] = month

        total_proposals = Suggestion.objects.filter(user=self.request.user).count()
        total_likes = Like.objects.filter(suggestion__user=self.request.user).count()

        monthly_proposals = Suggestion.objects.filter(user=self.request.user, created_at__year=year, created_at__month=month).count()
        monthly_likes = Like.objects.filter(suggestion__user=self.request.user, created_at__year=year, created_at__month=month).count()

        suggestion_queryset = Suggestion.objects.filter(created_at__year=year, created_at__month=month)
        df_line = read_frame(suggestion_queryset, fieldnames=['created_at'])
        df_line['created_at'] = pd.to_datetime(df_line['created_at'])
        df_line['day'] = df_line['created_at'].dt.date
        df_line = df_line.groupby('day').size()

        start_date = pd.Timestamp(year, month, 1)
        end_date = start_date + pd.offsets.MonthEnd(0)
        all_days = pd.date_range(start_date, end_date).date.tolist()

        days = []
        daily_suggestions = []
        for day in all_days:
            days.append(day.strftime('%Y-%m-%d'))
            daily_suggestions.append(df_line.get(day, 0))

        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        team_members = User.objects.filter(profile__department=self.request.user.profile.department)
        context['team_members'] = team_members
        context["current_user"] = self.request.user

        context.update({
            'total_proposals': total_proposals,
            'total_likes': total_likes,
            'monthly_proposals': monthly_proposals,
            'monthly_likes': monthly_likes,
            'days': days,
            'suggestions': daily_suggestions,
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,

        })

        return context


@login_required
def get_monthly_proposals(request):
    # Group by month and count the suggestions
    data = (
        Suggestion.objects
        .annotate(month=TruncMonth('created_at'))  # Extract the month
        .values('month')  # Group by the month
        .annotate(count=Count('id'))  # Count the suggestions
        .order_by('month')  # Order by the month
    )

    # Convert the QuerySet to a list of dictionaries
    data_list = list(data)

    # Return the data as JSON
    return JsonResponse(data_list, safe=False)



class FetchData(View):
    def get(self, request, *args, **kwargs):
        # Suggestionモデルのインスタンスを作成日の昇順で取得
        suggestions = Suggestion.objects.order_by('created_at')

        # データを整形
        data = [
            {
                "created_at": timezone.localtime(suggestion.created_at).isoformat(),
                "content": suggestion.content
            }
            for suggestion in suggestions
        ]

        # データをJSONとしてレスポンス
        return JsonResponse(data, safe=False)



@login_required
def get_weekly_proposals(request):
    # Group by week and count the suggestions
    data = (
        Suggestion.objects
        .annotate(week=TruncWeek('created_at'))  # Extract the week
        .values('week')  # Group by the week
        .annotate(count=Count('id'))  # Count the suggestions
        .order_by('week')  # Order by the week
    )

    # Convert the QuerySet to a list of dictionaries
    data_list = list(data)

    # Return the data as JSON
    return JsonResponse(data_list, safe=False)
