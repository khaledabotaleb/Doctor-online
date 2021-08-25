from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    AddClinicSerializer,
    AddReservationSerializer,
    DisplayClinicReservationSerializer
)
from clinic.authentication import SafeJWTAuthentication
from clinic.permissions import IsPatient, IsDoctor
from .models import Clinic, User, ClinicReservation


class RegisterUserApiView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        return serializer.save()


class LoginAPIView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        login_data = data.clean()
        return Response(login_data, status=status.HTTP_200_OK)


class AddClinicAPIView(generics.CreateAPIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    serializer_class = AddClinicSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, 201)


class ReserveClinicAPIView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    serializer_class = AddReservationSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(
            {"success": f"the clinic reserved successfully in time {serializer.data['reservation_time']}"},
            201
        )


class DisplayReservationAPIView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    serializer_class = DisplayClinicReservationSerializer

    def get(self, request):
        user = request.user
        user_clinics = user.clinic_user.all()
        clinic_reservations = ClinicReservation.objects.filter(clinic__in=user_clinics)
        serializer = self.serializer_class(clinic_reservations, many=True)
        return Response(serializer.data, 200)