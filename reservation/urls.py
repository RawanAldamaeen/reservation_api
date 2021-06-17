from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.patient_view import DoctorListView, NewReservationView
from .views.doctor_view import ReservationListView, ConfirmReservationView

urlpatterns = [
    path('reservation/new', NewReservationView.ReservationCreateView.as_view()),
    path('reservation/doctor-list', DoctorListView.DoctorsListView.as_view()),
    path('reservation/reservation-list', ReservationListView.ReservationsListView.as_view()),
    path('reservation/<int:pk>/confirm', ConfirmReservationView.ConfirmReservationView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)