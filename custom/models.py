from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.
GENDER_CHOICES = (
    ('f', 'female'),
    ('m', 'male'),
    ('r', 'rather not say ')
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(
	AbstractBaseUser,
	PermissionsMixin
):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250, blank=True)
    email = models.EmailField(
		verbose_name='email address', unique=True
	)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(
		upload_to="user_images", null=True, blank=True
	)
    gender = models.CharField(
		max_length=20, choices=GENDER_CHOICES, default="m"
	)
    
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    manager = models.BooleanField(default=False)  # a superuser
    username = None
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
	# notice the absence of a "Password field", that is built in.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff


class SiteSetting(models.Model):
    title = models.CharField(max_length=255)
    nav_color = models.CharField(max_length=20, default='#212529')
    body_color = models.CharField(max_length=20, default='#fff')

    def __str__(self):
        return self.title