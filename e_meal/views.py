from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *
from .filters import *
from .services import *

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all().order_by("-created")
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = MealFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by("created")
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IngredientFilter


# レシートをJSONに変換する
class RecieptConvertView(APIView):
    def post(self, request):
        if("receipt" not in request.POST):
            return Response("レシートの画像が必要です", status=406)

        try:
            service = ReceiptConvertService()
            return Response(
                service.convert(request.POST["receipt"]), 
                status=200)
        except CantFindValidDataError:
            return Response({
                'code': 'cant_find_valid_data'
                }, status=410)
        except Exception as ex:
            return Response({
                'code': 'developer_error',
                'message': ex
            }, status=500)
