from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .filters import *

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all().order_by("-created")
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = MealFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("-created")
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IngredientFilter
