from django.urls import path
from .views import (
    RegisterUserApiView,
    LoginAPIView,
    AddClinicAPIView,
    ReserveClinicAPIView,
    DisplayReservationAPIView
)

urlpatterns = [
    path('register/', RegisterUserApiView.as_view(), name='register-user'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('add_clinic/', AddClinicAPIView.as_view(), name='add-clinic'),
    path('add_reservation/', ReserveClinicAPIView.as_view(), name='reserve-clinic'),
    path('display_clinics/', DisplayReservationAPIView.as_view(), name='display-reserve')
]
