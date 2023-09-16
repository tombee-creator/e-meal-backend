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
            ser = IngredientSerializer(instance=Ingredient.objects.get(id=item["id"]), data=item)
            if ser.is_valid():
                obj = ser.save()
                MenuRelationship.objects.create(meal=instance, ingredient=obj, count=len(items))


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
