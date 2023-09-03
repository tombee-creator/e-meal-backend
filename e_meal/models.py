import uuid

from django.db import models

class Meal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('firebase_authentication.User', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MealPrep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('firebase_authentication.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    times = models.IntegerField(default=0)
    isUsedUp = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('firebase_authentication.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    times = models.IntegerField(default=0)
    isUsedUp = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
