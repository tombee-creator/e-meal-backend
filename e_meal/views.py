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
class ReceiptConvertView(APIView):
    def get(self, _):
        return Response({
            "version": "1.0.0",
            "message": "hello, i'm e-Meal receipt converter api. \nnow, i am learning hard.\nif my output results confuse you, i and my developer feel sorry.\nplease excuse.",
            "updated_log": "i can read japanese!! but it's not enough and i'm not satisfied at all. i'd like to learn more."
        }, status=200)
        
    def post(self, request):
        if("receipt" not in request.POST):
            return Response({
                'code': 'need_receipt'
            }, status=406)

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
            print(ex)
            return Response({
                'code': 'developer_error',
                'message': ex
            }, status=500)
