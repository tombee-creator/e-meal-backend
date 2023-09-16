import django_filters as filters
from .models import *

class MealFilter(filters.FilterSet):
    created_from = filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created', lookup_expr='lt')

    class Meta:
        model = Meal
        fields = [
            'id',
            'created_from',
            'created_to',
            'updated'
        ]

class IngredientFilter(filters.FilterSet):
    is_used_up = filters.BooleanFilter(field_name='is_used_up')
    category = filters.MultipleChoiceFilter(choices=Ingredient.CATEGORIES)
    created_from = filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created', lookup_expr='lt')

    class Meta:
        model = Ingredient
        fields = [
            'id', 
            'category',
            'created_from',
            'created_to',
            'updated',
            'is_used_up',
        ]
