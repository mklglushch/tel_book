from django.db import models
from django.contrib.auth.models import User


class Telephone_book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    type_contact = models.CharField(max_length=255)
    phone = models.TextField(max_length=12)
    email = models.TextField(max_length=255, blank=True)
    is_private = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username