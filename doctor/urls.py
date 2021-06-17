from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DoctorRegistrationView
from .views import DoctorActivationView
from .views import DoctorLoginView

urlpatterns = [
    path('doctor/new', DoctorRegistrationView.DoctorCreate.as_view()),
    path('doctor/login', DoctorLoginView.DoctorLoginView.as_view()),
    path('doctor/<int:pk>/activate', DoctorActivationView.DoctorActivation.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)