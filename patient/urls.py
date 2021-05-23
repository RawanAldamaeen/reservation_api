from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PatientRegistration
from .views import PatientActivationView

urlpatterns = [
    path('patient/new', PatientRegistration.PatientCreate.as_view()),
    path('patient/user-verify', PatientActivationView.VerifyUser.as_view(), name="user-verify"),

]

urlpatterns = format_suffix_patterns(urlpatterns)