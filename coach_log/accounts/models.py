from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from accounts.Validators import set_validate_birthday_or_none


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, first_name=None, last_name=None, birthday=None, avatar=None, about_me=None,
                    is_active=None, is_staff=None, is_admin=None
                    ):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The given password must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, birthday=birthday)
        user.set_password(password)
        user.staff = is_staff
        user.avatar = avatar
        user.about_me = about_me
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password,
                                is_staff=True, is_admin=True, is_active=True
                                )
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password,
                                is_staff=True, is_admin=False, is_active=True
                                )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        if not self.id and not self.staff and not self.admin:
            self.password = make_password(self.password)

        self.birthday = set_validate_birthday_or_none(self.birthday)
        super().save(*args, **kwargs)
