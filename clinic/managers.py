from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """Manager For User Profiles"""
    def create_user(self, email, password=None):
        """Create a new user profile """
        if not email:
            raise ValueError('User Must Have an Email Address')
        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user