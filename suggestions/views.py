from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Suggestion, Like ,Message # Like を追加
from .forms import SuggestionForm, UserProfileForm, MessageForm # UserProfileFormとMessageFormを追加
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # JsonResponseを追加
from django.views.decorators.http import require_POST  # require_POSTを追加





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
def message_create(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'suggestions/message_form.html', {'form': form, 'receiver': receiver})


@login_required
def message_list(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'suggestions/message_list.html', {'messages': messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user:
        raise Http404
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'suggestions/message_detail.html', {'message': message})
