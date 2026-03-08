# Building a CRUD API

## Introduction
So far, we have created a simple API route that returns a basic response. Now, let's build on this foundation by creating a CRUD API.

If you're unfamiliar with the term CRUD, it's an acronym that describes the four most common operations performed on data in an application:

| Operation | Description |
|---|---|
| C | **Create** data |
| R | **Retrieve** data |
| U | **Update** data |
| D | **Delete** data |

CRUD operations are essential for applications, especially those centered on data management. They form the foundation of business logic for handling data operations.

Since we're building a REST API, we should design it with CRUD principles in mind. Here's how we'll map HTTP methods to CRUD operations:

| Action | Method | Endpoint | Description |
|---|---|---|---|
| **Retrieve** | GET | `/api/v1/products` | List all products |
| **Retrieve** | GET | `/api/v1/products/<item_id>` | Get a specific product |
| **Create** | POST | `/api/v1/products/create` | Create a new product |
| **Update** | PATCH | `/api/v1/products/<item_id>/partially-update` | Partially update a product |
| **Update** | PUT | `/api/v1/products/<item_id>/update` | Fully update a product |
| **Delete** | DELETE | `/api/v1/products/<item_id>/delete` | Delete a product |

> ***Note***
>
> We are not using the RESTful approach to name our routes yet, but we shall orgnize the routes later for it to make sense

This mapping of HTTP requests to CRUD actions is the foundation for the API we'll build in this chapter.

## Setting Up the Django App for the CRUD
In the last chapter we created our project folder **core**, now let us create an app and register it o this project.

In our terminal, we shall run the command

```sh
python manage.py startapp products
```

This should create a new folder **products** in our current project folder, we need to register this in the **settings.py** located in the **core** project folder.

```py
# core/settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "products",
    # third party apps
    "rest_framework",
]
```

After doing this, we now have to populate our **views.py** of our new **products** app with the views.

```py
from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def product_list(request): ...

@api_view(["GET"])
def product_detail(request, pk): ...

@api_view(["POST"])
def product_create(request): ...

@api_view(["PATCH"])
def product_partial_update(request, pk): ...

@api_view(["PUT"])
def product_update(request, pk): ...

@api_view(["DELETE"])
def product_delete(request, pk): ...
```

We define the view functions and provide the appropriate methods using the `api_view` decorator. This decorator takes in the mandatory parameter of the  list of HTTP methods with which you will access the endpoints. 

Let us take it a little further by mapping these onto URLs that we shall use to access them. We are going to create a `urls.py` file and add the following to it. 

```py

# products/urls.py

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

```

We are using Django's way of mapping URLs to view functions to URLs inside the `urlpatterns` list. To make these available on our application, Let us now add the following code to the global URL configuration of our project.

```py
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
    path("products/", include("products.urls")), #add this
]

```
