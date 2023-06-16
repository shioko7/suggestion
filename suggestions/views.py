from django.shortcuts import render, redirect,get_object_or_404
from .forms import SuggestionForm
from .models import Category, Suggestion
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm




def index(request):
    return render(request, 'suggestions/index.html')

@login_required
def suggestion_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suggestion_list')
    else:
        form = SuggestionForm()
    return render(request, 'suggestions/create.html', {'form': form, 'categories': categories})


@login_required
def suggestion_list(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'suggestions/list.html', {'suggestions': suggestions})


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
    if request.user != suggestion.user:
        return redirect('suggestion_list')

@login_required
def suggestion_delete(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    if request.user != suggestion.user:
        return redirect('suggestion_list')


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
