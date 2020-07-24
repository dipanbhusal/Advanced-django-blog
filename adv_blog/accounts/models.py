from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager)
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.timezone import now
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email:
            raise ValueError('Email is required')
        
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, password = None):
        user = self.create_user(
            email, 
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class UserModel(AbstractBaseUser):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(verbose_name='Email Address',
        max_length=255,
        unique=True
        )

    created_at = models.DateTimeField(auto_now=now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default = False) 
    username = models.CharField(max_length=100, blank = True)
    profile_picture = models.ImageField(upload_to='profile_pics', default = 'profile_pics/default.jpg')
    bio = models.TextField(blank=True)
    email_confirmed = models.BooleanField(default = False)
    objects = UserManager()
    groups = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ ]

    def save(self, *args, **kwargs):
        username = self.email.split('@')
        self.username = username[0]
        print(self.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        return self.is_admin
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('accounts:profile', kwargs={'slug': self.username})

