from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, account_id, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, account_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    account_id = models.CharField(max_length=50, unique=True, verbose_name=_("Account ID"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=150, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=150, verbose_name=_("Last Name"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    favorite_products = models.ManyToManyField(
        'search_app.Product',
        related_name='favorited_products',  # related_name を変更
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_id', 'first_name', 'last_name']

    def __str__(self):
        return self.account_id
