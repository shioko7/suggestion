# suggestions/my_context_processor.py
from django.utils import timezone

def common(request):
    """Suggestion app's common context"""
    now = timezone.now()

    return {"now_year": now.year,
            "now_month": now.month}
