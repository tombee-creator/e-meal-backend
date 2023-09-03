from rest_framework import serializers
from rest_framework.permissions import AllowAny
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
        return ret


class MealPrepSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPrep
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
