from ulid import ULID

from django.db import models

from django.contrib.auth.models import AbstractUser

class FirebaseUser(AbstractUser):
    USERNAME_FIELD = 'firebase_uid'
    
    firebase_uid = models.CharField(primary_key=True, max_length=128, db_index=True, unique=True)
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Meal(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=ULID, editable=False)
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
    preps = models.ManyToManyField("Ingredient", related_name="preps", through="MenuRelationship")
    
    def get_cost(self):
        items = self.preps.all()
        if len(items) == 0:
            return self.cost
        return sum(list(map(
            lambda item: item.get_cost() * self.get_used_count(item) / 
                self.get_all_used_count(item), 
            self.preps.all())))
    
    def get_used_count(self, item):
        rel = MenuRelationship.objects.get(meal=self, ingredient=item)
        return rel.count
    
    def get_all_used_count(self, ingredient):
        as_ingredient_count = sum(list(map(lambda rel: rel.count, 
            RecipeRelationship.objects.filter(ingredient=ingredient))))
        as_prep_count = sum(list(map(lambda rel: rel.count, 
            MenuRelationship.objects.filter(ingredient=ingredient))))
        return as_ingredient_count + as_prep_count


class MenuRelationship(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=ULID, editable=False)
    meal = models.ForeignKey(
        "Meal", 
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        "Ingredient", 
        on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    CATEGORIES = (
        (0, 'ingredient'),
        (1, 'prep'),
        (2, 'gift')
    )
    
    id = models.CharField(max_length=26, primary_key=True, default=ULID, editable=False)
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
    category = models.IntegerField(choices=CATEGORIES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipe = models.ManyToManyField(
        "Ingredient", 
        related_name="recipe_set", 
        through="RecipeRelationship")
    
    def get_cost(self):
        items = self.recipe.all()
        if len(items) == 0:
            return self.cost

        # 使用済み回数を計算
        used_count = sum(list(
            map(lambda rel: rel.count, 
            RecipeRelationship.objects.filter(prep=self))))
        return sum(list(map(
            lambda rel: rel.ingredient.get_cost() * used_count / rel.ingredient.get_all_used_count(),
            RecipeRelationship.objects.filter(prep=self))))
    
    def get_all_used_count(self):
        as_ingredient_count = sum(list(map(lambda rel: rel.count, 
            RecipeRelationship.objects.filter(ingredient=self))))
        as_prep_count = sum(list(map(lambda rel: rel.count, 
            MenuRelationship.objects.filter(ingredient=self))))
        return as_ingredient_count + as_prep_count

class RecipeRelationship(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=ULID, editable=False)
    prep = models.ForeignKey(
        "Ingredient",
        on_delete=models.CASCADE,
        related_name="prep")
    ingredient = models.ForeignKey(
        "Ingredient",
        on_delete=models.CASCADE,
        related_name="ingredient")
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
