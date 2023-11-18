from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from helpers.models import BaseModel


class CustomUserManager(BaseUserManager):
    """
    Manager class for custom User model.

    This manager defines methods to create regular users and superusers, as well as
    to query for active users or all users regardless of their active status.

    Methods:
        create_user(self, email, password=None, **extra_fields): Creates a regular user.
        create_superuser(self, email, password=None, **extra_fields): Creates a superuser.
        active(self): Returns a QuerySet of active users.
        all_objects(self): Returns a QuerySet of all users, active and inactive.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password of the user.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created user instance.
        """

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password of the user.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created superuser instance.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def active(self):
        """
        Returns a QuerySet of active users.

        Returns:
            QuerySet: A QuerySet of active user instances.
        """

        return self.get_queryset().filter(is_active=True)

    def all_objects(self):
        """
        Returns a QuerySet of all users, active and inactive.

        Returns:
            QuerySet: A QuerySet of all user instances.
        """

        return self.get_queryset().all()


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    User model that represents a user in the system.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        full_name (str): The user's full name, automatically generated from first and last names.
        email (str): The user's email address. Must be unique.
        is_active (bool): A flag indicating if the user account is active. Defaults to True.
        is_staff (bool): A flag indicating if the user is a staff member. Defaults to False.
        inactivation_date (datetime): The date and time when the user was inactivated.
            Null if the user is active.
        groups (ManyToManyField): The groups this user belongs to.
        user_permissions (ManyToManyField): The specific permissions for this user.
    """

    first_name = models.CharField(
        max_length=50,
        verbose_name=_('First Name'),
        help_text=_('User First Name')
    )
    last_name = models.CharField(
        max_length=250,
        verbose_name=_('Last Name'),
        help_text=_('User Last Name')
    )
    full_name = models.CharField(
        max_length=301,
        verbose_name=_('Full Name'),
        help_text=_('User Full Name')
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name=_('Email'),
        help_text=_('User Email')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'),
        help_text=_('User Active Status')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Is Staff'),
        help_text=_('User Staff Status')
    )
    inactivation_date = models.DateTimeField(
        null=True,
        verbose_name=_('Inactivation Date'),
        help_text=_('User Inactivation Date')
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'account_user'

    def __str__(self):
        return self.full_name or ""

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'.strip()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.is_active:
            return
        self.is_active = False
        self.inactivation_date = timezone.now()
        self.save()
