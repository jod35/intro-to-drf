from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product

# Create your views here.


@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def product_detail(request, pk): ...


@api_view(["POST"])
def product_create(request): ...


@api_view(["PATCH"])
def product_partial_update(request, pk): ...


@api_view(["PUT"])
def product_update(request, pk): ...


@api_view(["DELETE"])
def product_delete(request, pk):
    pass
