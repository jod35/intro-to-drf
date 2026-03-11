from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.


@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(data=serializer.data, status=200)


@api_view(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(
            data={"error": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def product_create(request):
    data = request.data
    serializer = ProductCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            data={"message": "Product added successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = request.data
        serializer = ProductCreateSerializer(data=data, instance=product)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "message": "Product updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response(
            data={"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(
            data={"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
