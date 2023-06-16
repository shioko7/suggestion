from django.shortcuts import render, redirect
from .forms import SuggestionForm
from .models import Category, Suggestion

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

def suggestion_list(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'suggestions/list.html', {'suggestions': suggestions})
