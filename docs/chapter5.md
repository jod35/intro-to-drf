# Class-Based Views

## Introduction
This chapter explains how to leverage DRF's class-based views to build cleaner, more maintainable APIs with less boilerplate code. Class-based views provide an object-oriented approach that replaces function-based decorators with structured class methods.

## Create your first API View
Compare the function-based **Hello World** view from **core/urls.py**:

```py
# core/urls.py

from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_world(request):
    return Response(data={"message": "Hello, World!"}, status=200)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello_world, name="hello_world"),
    path("products/", include("products.urls")),
]
```

With its class-based equivalent:

```py
# core/urls.py

class HelloWorldView(APIView):
    def get(self, request):
        return Response(data={"message": "Hello, World!"}, status=200)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HelloWorldView.as_view(), name="hello_world"),
    path("products/", include("products.urls")),
]
```

All DRF class-based views inherit from `APIView`. HTTP methods (`get`, `post`, `put`, etc.) become class methods that directly correspond to request types. Use the `as_view()` method when registering views in your URL configuration.

## Refactor existing views

Convert all API views in **products/views.py** to class-based views:

```py

# products/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                data={"error": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

class ProductCreateView(APIView):
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Product added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductCreateSerializer(data=request.data, instance=product)
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
                data={"error": "Product does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

class ProductDeleteView(APIView):
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(
                data={"error": "Product does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
```

Each class inherits from `APIView` and implements HTTP methods instead of using decorators. Update **products/urls.py** to use the `as_view()` method:

```py

# core/urls.py

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("create/", views.ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),
]
```

## Generic Views
DRF's generic views further reduce boilerplate by automating common patterns. They integrate with your models and serializers to handle standard operations. Customize them to fit your specific requirements and business logic.

Let us modify the views in **products/views.py** to have this 

```py

# products/views.py

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    serializer_class = ProductCreateSerializer


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

We have in-built classes like the `CreateAPIView`, `ListAPIView`, `RetrieveAPIView`, `UpdateAPIView` and `DeleteAPIView`. The only have to be pointed to a model and the right serializer and your CRUD will be built.

## REST-style Endpoints
Remember we have not yet achieved the proper RESTful way of defining our endpoints. So let us achieve that with DRF. Let us further modify the views to look like this.

```py
# products/views.py 

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return super().get_serializer_class()


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductCreateSerializer
        return super().get_serializer_class()

```