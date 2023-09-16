import json
from rest_framework import serializers
from .models import *

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super(MealSerializer, self).to_representation(instance)
        ret['user'] = {
            'username': instance.user.firebase_uid,
            'email': instance.user.email,
        }
        ret['preps'] = list(map(
            lambda prep: self.to_representation_meal_prep(prep, instance), 
            instance.preps.all()))
        return ret

    def to_representation_meal_prep(self, prep, meal):
        ser = IngredientSerializer(prep)
        ret = ser.data
        relationship = MenuRelationship.objects.get(meal=meal, ingredient=prep)
        ret["used_count"] = relationship.count
        return ret

    def save(self, **kwargs):
        initial_data = self.initial_data
        print(initial_data)
        instance = super().save(**kwargs)
        recipe_data = json.loads(initial_data["menu"])
        if recipe_data != None:
            self.save_recipe_data(instance, recipe_data)
        return instance

    def save_recipe_data(self, meal, recipe_data):
        for data in recipe_data:
            ingredient = Ingredient.objects.get(pk=data["ingredient"])
            print(ingredient)
            ingredient.is_used_up = data['is_used_up']
            ingredient.save()
            MenuRelationship.objects.create(
                meal=meal,
                ingredient=ingredient,
                count=data["count"])


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(IngredientSerializer, self).to_representation(instance)
        ret['user'] = {
            'username': instance.user.firebase_uid,
            'email': instance.user.email,
        }
        relationships = RecipeRelationship.objects.filter(ingredient=instance)
        ret["used_count"] = sum(map(lambda relationship: relationship.count, relationships))
        return ret

    def save(self, **kwargs):
        initial_data = self.initial_data
        instance = super().save(**kwargs)
        recipe_data = json.loads(initial_data["recipe"])
        if recipe_data != None:
            self.save_recipe_data(instance, recipe_data)
        return instance

    def save_recipe_data(self, prep, recipe_data):
        for data in recipe_data:
            ingredient = Ingredient.objects.get(pk=data["ingredient"])
            ingredient.is_used_up = data['is_used_up']
            ingredient.save()
            RecipeRelationship.objects.create(
                prep=prep,
                ingredient=ingredient,
                count=data["count"])
