import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser


class FirebaseUser(AbstractUser):
    USERNAME_FIELD = 'firebase_uid'
    
    firebase_uid = models.CharField(primary_key=True, max_length=128, db_index=True, unique=True)
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Meal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preps = models.ManyToManyField("MealPrep", related_name="preps", through="MealRelationship")


class MealRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE)
    meal_prep = models.ForeignKey("MealPrep", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MealPrep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    times = models.IntegerField(default=0)
    is_used_up = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipe = models.ManyToManyField("Ingredient", related_name="recipe", through="RecipeRelationship")


class RecipeRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal_prep = models.ForeignKey("MealPrep", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    url = models.URLField(blank=True)
    cost = models.FloatField(
        verbose_name='',
        blank=True,
        null=True,
        default=0.0)
    times = models.IntegerField(default=0)
    is_used_up = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
