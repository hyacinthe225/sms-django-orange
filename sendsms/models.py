import csv, io
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

class Verif(models.Model):
    code_user = models.CharField(max_length=4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    vcode = models.CharField(max_length=6)
    tel_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.nom

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Sms(models.Model):
    address = models.CharField(max_length=15, blank=True, null=True)
    senderAddress = models.CharField(max_length=15)
    message = models.CharField(max_length=200)
    groupe = models.CharField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add = True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.address

class Groupe(models.Model):
    groupe = models.CharField(max_length=50, blank=True , null=True)
    nom = models.CharField(max_length=50)
    numeros = models.CharField(max_length=5000)
    def __str__(self):
        return self.groupe


class Liste(models.Model):
    nom = models.CharField(max_length=50)
    numeros = models.CharField(max_length=80000)
