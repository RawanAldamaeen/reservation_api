from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateShiftView

urlpatterns = [
    path('shift/new', CreateShiftView.ShiftCreateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)