from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

from .managers import MyUserManager


class TimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'Time Stamp'


class User(AbstractBaseUser, PermissionsMixin, TimeBase):
    USER_TYPE = (
        ('doctor', 'doctor'),
        ('patient', 'patient')
    )
    email = models.EmailField(_('email address'), validators=[validate_email], max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    city = models.CharField(max_length=50)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'User'

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Clinic(TimeBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_user')
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'Clinic'

    def __str__(self):
        return self.name


class ClinicReservation(TimeBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reserve_user')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reserve_clinic')
    reservation_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'Reservation'
