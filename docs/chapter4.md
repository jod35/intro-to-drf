# Building a CRUD API

## Introduction
We've created a simple API route that returns a basic response. Now let's expand on this foundation by building a complete CRUD API.

CRUD is an acronym representing the four fundamental operations performed on data in an application:

| Operation | Description |
|---|---|
| C | **Create** data |
| R | **Retrieve** data |
| U | **Update** data |
| D | **Delete** data |

CRUD operations are essential for data-driven applications and form the foundation of business logic for handling data persistence and manipulation.

For a REST API, we should design endpoints using CRUD principles. Here's how we map HTTP methods to CRUD operations:

| Action | Method | Endpoint | Description |
|---|---|---|---|
| **Retrieve** | GET | `/api/v1/products` | List all products |
| **Retrieve** | GET | `/api/v1/products/<item_id>` | Get a specific product |
| **Create** | POST | `/api/v1/products/create` | Create a new product |
| **Update** | PUT | `/api/v1/products/<item_id>/update` | Fully update a product |
| **Delete** | DELETE | `/api/v1/products/<item_id>/delete` | Delete a product |

> ***Note***
>
> We're not following RESTful naming conventions yet, but we'll refactor our routes later to follow best practices.

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
    path("api/products/", include("products.urls")),
]
```

## Creating the Model
Now let's add the data model for our application. In the **models.py** file of the products app, add the following code:

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

This creates a `Product` model that forms the basis of our simple application. The model includes fields for product name, description, price, and stock quantity.

Next, register this model with Django Admin. Add the following code to **products/admin.py**:

```py
# products/admin.py
from django.contrib import admin

from products.models import Product

# Register your models here.

admin.site.register(Product)
```

Stop your server and run the following command to create a migration file for the model:

```sh
python manage.py makemigrations
```

Then apply the migration to your database:

```sh
python manage.py migrate
```

## The Django Admin App
To manage our products through Django's built-in admin interface, we need to create a superuser account.

Run the following command:

```sh
python manage.py createsuperuser
```

Restart your server and navigate to **http://localhost:8000/admin**. Log in with your superuser credentials. You should see the Django admin dashboard:

![django admin](./imgs/django%20admin.png)

Create a product through the admin interface:

![create product](./imgs/create%20product.png)

After saving, you'll see the product listed:

![Saved product](./imgs/product%20added.png)

Add as many products as you need for testing.

## Building the CRUD Endpoints

### Read (List) Items
Let's start by implementing the endpoint for listing all product items.

```py
# products/views.py

from rest_framework.decorators import api_view
from .models import Product

# Create your views here.


@api_view(["GET"])
def product_list(request): 
    products = Product.objects.all()
    ...

# ... more api views here
```

In our `product_list` view, we query the database to retrieve all products. However, we need to serialize these database objects into JSON format so clients can consume the data.

Create a new file called **serializers.py** in the **products** app:

```py
from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

The `ProductSerializer` class is responsible for converting Product model instances to JSON. Django REST Framework's `ModelSerializer` base class simplifies this process significantly.

Now modify the view to return a properly serialized response:

```py
# products/views.py

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

We instantiate `ProductSerializer` with our queryset and set `many=True` because we're serializing a list of products. The serializer converts the data to JSON format.

Navigate to **http://localhost:8000/api/products** to see the list:

![List all products](./imgs/lis%20all%20products.png)

### Create Item
Let's create a dedicated serializer for adding products. This allows us to specify which fields users can submit when creating a product:

```py
# products/serializers.py

from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock"]
```

The `ProductCreateSerializer` specifies exactly which fields are required for product creation, similar to a form.

Update your views to implement the create endpoint:

```py
# products/views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, ProductCreateSerializer
from .models import Product

# Create your views here.

# ... more code here

@api_view(["POST"])
def product_create(request):
    serializer = ProductCreateSerializer(request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            data={
                "message": "Product added successfully",
                "data": serializer.data
            }, 
            status=status.HTTP_201_CREATED
        )
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

This endpoint receives data from the client, validates it through `ProductCreateSerializer`, and saves it if valid. If validation fails, it returns error details.

Navigate to **http://localhost:8000/api/products/create** to test the endpoint:

![product create on browsable API DRF](./imgs/product%20create%20browsable%20API%20DRF.png)

Django REST Framework provides a user-friendly interface for testing API endpoints. If you submit invalid data, you'll see validation errors:

![product create on browsable API with errors](./imgs/product%20create%20browsable%20API%20with%20errors.png)

Submitting valid data returns a successful response:

![product create on browsable API successful](./imgs/product%20create%20success.png)

### Read (Retrieve) an Item
To retrieve an item by ID, add the following code to **products/views.py**:

```py
# products/views.py

# ... other code here
@api_view(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(
            data={"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )
```

To retrieve an item, we query the database for a product with the given `pk` and use our `ProductSerializer` class to convert it to JSON format. If the product is not found, we return an error with a 404 status code; otherwise, we return a successful response with the item.

To test this endpoint, navigate to **http://localhost:8000/api/products/1**:

![retrieve product on Browsable API](./imgs/get%20product%20by%20ID.png)

Now let's test retrieving a product with an ID that doesn't exist in the database:

![retrieve non-existent item](./imgs/get%20non%20existent%20product.png)

### Update an Item
Add the following code to your views:

```py
@api_view(["PATCH"])
def product_update(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductCreateSerializer(data=request.data, instance=product)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "message": "Product updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response(
            data={"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
```

This view retrieves the product with the given `pk`. If not found, it returns a 404 error. Otherwise, it validates the update data using `ProductCreateSerializer`. If valid, it saves the changes and returns a success response; otherwise, it returns any validation errors.

Testing the update endpoint looks like this:

![updating the product](./imgs/Successful%20update.png)

### Delete an Item
To delete an item, query for it, delete it, and return the appropriate status code:

```py
# products/views.py

@api_view(["DELETE"])
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(
            data={"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
```

![Delete request in Postman](./imgs/postman%20delete%20request.png)

In this example, I'm using an actual API client, [Postman](https://www.postman.com/), to make the request. While Django REST Framework's browsable API can handle DELETE requests through class-based views, those are topics we'll explore in the next chapter.

