from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET", "POST"])
def product_list_or_create(request): ...


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
