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
            'username': instance.user.username,
            'email': instance.user.email,
        }
        ret['preps'] = list(map(
            lambda prep: self.to_representation_meal_prep(prep, instance), 
            instance.preps.all()))
        return ret

    def to_representation_meal_prep(self, prep, meal):
        ser = MealPrepSerializer(prep)
        ret = ser.data
        relationship = MealRelationship.objects.get(meal=meal, meal_prep=prep)
        ret["used_count"] = relationship.count
        return ret

    def save(self, **kwargs):
        initial_data = self.initial_data
        instance = super().save(**kwargs)
        prep_data = json.loads(initial_data["preps"])
        if prep_data != None:
            self.save_prep_data(instance, prep_data)
        return instance

    def save_prep_data(self, instance, prep_data):
        ids = set(map(lambda prep: prep["id"], prep_data))
        for id in ids:
            items = list(filter(lambda item: item["id"] == id, prep_data))
            item = items[-1]
            ser = MealPrepSerializer(instance=MealPrep.objects.get(id=item["id"]), data=item)
            if ser.is_valid():
                obj = ser.save()
                MealRelationship.objects.create(meal=instance, meal_prep=obj, count=len(items))


class MealPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPrep
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(MealPrepSerializer, self).to_representation(instance)
        ret['user'] = {
            'username': instance.user.username,
            'email': instance.user.email,
        }
        relationships = MealRelationship.objects.filter(meal_prep=instance)
        ret["used_count"] = sum(map(lambda relationship: relationship.count, relationships))
        return ret

    def save(self, **kwargs):
        initial_data = self.initial_data
        instance = super().save(**kwargs)
        recipe_data = json.loads(initial_data["recipe"])
        if recipe_data != None:
            self.save_recipe_data(instance, recipe_data)
        return instance

    def save_recipe_data(self, instance, recipe_data):
        ids = set(map(lambda recipe: recipe["id"], recipe_data))
        for id in ids:
            items = list(filter(lambda item: item["id"] == id, recipe_data))
            item = items[-1]
            ser = IngredientSerializer(instance=Ingredient.objects.get(id=item["id"]), data=item)
            if ser.is_valid():
                obj = ser.save()
                RecipeRelationship.objects.create(meal_prep=instance, ingredient=obj, count=len(items))
            

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(IngredientSerializer, self).to_representation(instance)
        ret['user'] = {
            'username': instance.user.username,
            'email': instance.user.email,
        }
        relationships = RecipeRelationship.objects.filter(ingredient=instance)
        ret["used_count"] = sum(map(lambda relationship: relationship.count, relationships))
        return ret
