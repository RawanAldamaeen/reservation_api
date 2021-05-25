from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PatientRegistration

urlpatterns = [
    path('patient/new', PatientRegistration.PatientCreate.as_view()),
    path('patient/email-verify', PatientRegistration.VerifyEmail.as_view(), name="email-verify"),

]

urlpatterns = format_suffix_patterns(urlpatterns)