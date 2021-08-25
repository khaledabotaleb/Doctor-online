from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

from .models import User, Clinic, ClinicReservation
from .utils import generate_access_token, generate_refresh_token


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(min_length=8, required=True, allow_null=False,
                                     style={'input_type': 'password', 'placeholder': 'Password'},
                                     write_only=True
                                     )
    confirm_password = serializers.CharField(min_length=8, required=True, allow_null=False,
                                             style={'input_type': 'password', 'placeholder': 'Password'},
                                             write_only=True
                                             )

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'user_type', 'phone_number',
                  'city']

    def clean_email(self):
        email = self.validated_data['email']
        try:
            user = self.Meta.model.objects.get(email=email)
            raise exceptions.ValidationError({'email': [_('Email already exist')]})
        except ObjectDoesNotExist:
            return email

    def clean_password(self):
        password1 = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        if password2 != password1:
            raise exceptions.ValidationError({'password': [_('Password not match')]})
        return password1

    def save(self, **kwargs):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_type=self.validated_data['user_type'],
            phone_number=self.validated_data['phone_number'],
            city=self.validated_data['city'],
        )
        email = self.clean_email()
        user.email = email
        password = self.clean_password()
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(min_length=8, required=True, allow_null=False)

    User = get_user_model()

    def clean(self):
        email = self.validated_data['email']
        pwd = self.validated_data['password']
        try:
            user = self.User.objects.get(email=email)
            if not user.check_password(pwd):
                # raise serializers.ValidationError()
                raise exceptions.ValidationError({'password': [_('Wrong password')]})
            access_token = generate_access_token(user)
            token_version = user.auth_token.key
            refresh_token = generate_refresh_token(user, token_version)
            return {
                'access_token': access_token, 'refresh_token': refresh_token, 'id': user.id, 'user_type': user.user_type
            }
        except User.DoesNotExist:
            raise exceptions.ValidationError({'email': [_('Not found')]})


class AddClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        exclude = ('user', )


class AddReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicReservation
        fields = ['clinic', 'reservation_time']


class DisplayClinicReservationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    clinic_name = serializers.SerializerMethodField()
    clinic_date = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = ClinicReservation
        fields = ['user', 'clinic_name', 'clinic_date', 'doctor', 'reservation_time']

    def get_user(self, obj):
        user = obj.user
        return user.get_full_name()

    def get_clinic_name(self, obj):
        return obj.clinic.name

    def get_clinic_date(self, obj):
        return obj.clinic.date

    def get_doctor(self, obj):
        return obj.clinic.user.get_full_name()
