from rest_framework import serializers
from .models import *

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
    
    def to_representation(self, instance):
        ret = super(MealSerializer, self).to_representation(instance)
        ret['user'] = {
            'id': instance.user.id,
            'email': instance.user.email,
        }
        ret['preps'] = list(map(
            lambda prep: self.to_representation_meal_prep(prep, instance), 
            instance.preps.all()))
        return ret

    def to_representation_meal_prep(self, prep, meal):
        ser = MealPrepSerializer(prep)
        ret = ser.data
        relationship = MealRelationship.objects.get(meal=meal, mealPrep=prep)
        ret["used_count"] = relationship.count
        return ret


class MealPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPrep
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(MealPrepSerializer, self).to_representation(instance)
        ret['user'] = {
            'id': instance.user.id,
            'email': instance.user.email,
        }
        return ret

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(IngredientSerializer, self).to_representation(instance)
        ret['user'] = {
            'id': instance.user.id,
            'email': instance.user.email,
        }
        return ret
