from . import views
from django.urls import path

urlpatterns = [
    path("", views.ProductListCreateView.as_view(), name="product-list"),
    path(
        "<int:pk>/",
        views.ProductRetrieveUpdateDestroyView.as_view(),
        name="product-detail",
    ),
]
