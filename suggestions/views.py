from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Suggestion, Like ,Message # Like を追加
from .forms import SuggestionForm, UserProfileForm, MessageForm # UserProfileFormとMessageFormを追加
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # JsonResponseを追加
from django.views.decorators.http import require_POST  # require_POSTを追加
from django.contrib.auth.models import User  # Userモデルのインポートを追加
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncDay,TruncMonth
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.db.models.functions import TruncWeek
from django_pandas.io import read_frame
import pandas as pd
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin








def index(request):
    return render(request, 'suggestions/index.html')

@login_required
def suggestion_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            return redirect('suggestion_list')
    else:
        form = SuggestionForm()
    return render(request, 'suggestions/create.html', {'form': form, 'categories': categories})


@login_required
def suggestion_list(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'suggestions/list.html', {'suggestions': suggestions})


# いいね機能のためのビューを追加
@login_required
@require_POST  # POSTメソッドのみを受け付けるようにする
def like_suggestion(request):
    """Suggestionのいいね処理"""
    suggestion_id = request.POST.get('post_pk')  # POSTデータからsuggestion_idを取得
    suggestion = get_object_or_404(Suggestion, pk=suggestion_id)
    like = Like.objects.filter(suggestion=suggestion, user=request.user)
    context = {}
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        Like.objects.create(suggestion=suggestion, user=request.user)
        context['method'] = 'create'
    #該当の投稿のいいねの数を取得
    context['like_count'] = Like.objects.filter(suggestion=suggestion).count()
    return JsonResponse(context)



@login_required
def suggestion_detail(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    return render(request, 'suggestions/suggestion_detail.html', {'suggestion': suggestion})


def home(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:
        return redirect('login')

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
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    if request.method == 'POST':
        suggestion.delete()
        return redirect('suggestion_list')
    return render(request, 'suggestions/suggestion_delete.html', {'suggestion': suggestion})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'suggestions/profile.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'suggestions/edit_profile.html', {'form': form})

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

        # これから表示する年月
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['now_year'] = year
        context['now_month'] = month

        total_proposals = Suggestion.objects.filter(user=self.request.user).count()
        total_likes = Like.objects.filter(suggestion__user=self.request.user).count()

        # 当月の提案数を取得
        monthly_proposals = Suggestion.objects.filter(user=self.request.user, created_at__year=year, created_at__month=month).count()

        # 当月のいいね数を取得
        monthly_likes = Like.objects.filter(suggestion__user=self.request.user, created_at__year=year, created_at__month=month).count()

        # 今月の提案の日付ごとの件数を取得
        suggestion_queryset = Suggestion.objects.filter(created_at__year=year, created_at__month=month)
        df_line = read_frame(suggestion_queryset, fieldnames=['created_at'])
        df_line['created_at'] = pd.to_datetime(df_line['created_at'])
        df_line['day'] = df_line['created_at'].dt.strftime('%Y-%m-%d')
        df_line = df_line.groupby('day').size()
        days = [day for day in df_line.index.values]
        daily_suggestions = [val for val in df_line.values]

        # 前月と次月をコンテキストに入れて渡す
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
            'next_month': next_month
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
