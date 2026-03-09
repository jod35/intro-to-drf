# Building a CRUD API

## Introduction
We've created a simple API route that returns a basic response. Now let's expand on this foundation by building a CRUD API.

CRUD is an acronym representing the four fundamental operations performed on data in an application:

| Operation | Description |
|---|---|
| C | **Create** data |
| R | **Retrieve** data |
| U | **Update** data |
| D | **Delete** data |

CRUD operations are essential for data-driven applications and form the foundation of business logic for handling data.

For a REST API, we should design endpoints using CRUD principles. Here's how we'll map HTTP methods to CRUD operations:

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
> We're not using the RESTful naming convention yet, but we'll refactor our routes later to follow best practices.

This mapping of HTTP requests to CRUD actions forms the foundation for the API we'll build in this chapter.

## Setting Up the Django App for CRUD
In the previous chapter, we created the **core** project folder. Now let's create an app and register it with the project.

Run the following command in your terminal:

```sh
python manage.py startapp products
```

This creates a new **products** folder in your project. Next, register it in **core/settings.py**:

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

Now, populate **products/views.py** with the view functions:

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

The `@api_view` decorator specifies which HTTP methods are allowed for each endpoint.

Next, create **products/urls.py** to map these views to URL endpoints:

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

Finally, include these URLs in your project's main URL configuration:

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
## Creating the model
Let us now add the data model for this simple app. In the **models.py** for the products app, let us add the following code.

```py
# products/models.py
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

```

This will create a `Product` model that will form the basis of the simple application. Let us register this app to be accessed on the admin. Add the following code in your **admin.py** in the product app.

```py
# products/admin.py
from django.contrib import admin

from products.models import Product

# Register your models here.

admin.site.register(Product)

```


Stop our server and run the following command.

```sh
python manage.py makemigrations
```

This will create the migration file for the model we have created.

```sh
python manage.py migrate
```

This will apply the changes to the database.

## The Django Admin app
We will have to make our model exist on the admin dashboard in-built into Django. To do this, we shall to create a superuser to access the admin dashboard.

Run the following command

```sh
python manage.py createsuperuser
```

Let us re-run our server and navigate to **http://localhost:8000/admin**. Login with your created superuser and you will see the following.

![django admin](./imgs/django%20admin.png)

Create a product like this

![create product](./imgs/create%20product.png)

Save Product

![Saved product](./imgs/product%20added.png)

Add as many products as you may want.

## Build the CRUD

Let us start by building the CRUD.

```py
# products/views.py

from rest_framework.decorators import api_view
from .models import Product

# Create your views here.


@api_view(["GET"])
def product_list(request): 
    products = Product.objects.
    ...

# ... more api views here
```

Under our `product_list` view, is gonna be a query to return all products from the db. We need to serailize that list of database model objects into JSON which we shall then provide to clients.

Let us create a new file **serializers.py** in the current **products** app. 

```py
from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

```

We have created a class called the `ProductSerializer` class whose responsibility is to serialize Product model objects to JSON. DRF provides the `serializers.ModelSerializer` class that makes it easy to do so.

Let us now modify the view to return a reponse with the data.

```py
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
```

What we have done here is to create a `ProductSerializer` instance with the queryset object we have got from the database, we have added the `many` argument because we want to rturn a list of `Product`s.

Let us now navigate to **http://localhost:8000/products**

![List all products](./imgs/lis%20all%20products.png)