from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ProductCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import Product

# Create your views here.

class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = Product
        fields = []


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_class = ItemFilter
    permission_classes = [IsAuthenticated]


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
