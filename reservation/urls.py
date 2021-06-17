from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NewReservationView
from .views import DoctorListView

urlpatterns = [
    path('reservation/new', NewReservationView.ReservationCreateView.as_view()),
    path('reservation/doctor-list', DoctorListView.DoctorsListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)