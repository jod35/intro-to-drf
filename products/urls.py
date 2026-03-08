from . import views
from django.urls import path

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("<int:pk>/", views.product_detail, name="product-detail"),
    path("create/", views.product_create, name="product-create"),
    path("<int:pk>/update/", views.product_update, name="product-update"),
    path(
        "<int:pk>/partial-update/",
        views.product_partial_update,
        name="product-partial-update",
    ),
    path("<int:pk>/delete/", views.product_delete, name="product-delete"),
]
