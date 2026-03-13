## Authentication

Authentication basically refers to the action of associating each request with information about it so that way we can either grant or restrict access to resources. DRF has in-built approaches to ths but also gives you freedom to implement and use custom schemes.

## Token Based authentication
Token authentication is a method where a user proves their identity to an API by sending a unique secret token instead of sending their username and password with every request. DRF provides an in-built app to help you carry out simple token authentication. It can be set up in the following way.

```py
INSTALLED_APPS = [
    # ... other apps
    # third party apps
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters"
]

# ... other settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ]
}
```

To create a token for a user given a username, You run the following command. 


```sh
python3 manage.py drf create_token <username>
```

This creates a token which will be used by the user to login using the authorization header `Token <token>`

You can also implement a signal to create tokens for users everytime you create their accounts.

```py

# in a signals.py
# from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 
```

You then have to setup the endpoint you will use to aquire the token.

```py
# ... other code here
from rest_framework.authtoken.views import obtain_auth_token

# ... other code here

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HelloWorldView.as_view(), name="hello_world"),
    path("products/", include("products.urls")),
    path("auth/token",obtain_auth_token) # add this
]

```

Endpoints are then protected by adding a list of authentication classes like:

```py
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_class = ItemFilter
    permission_classes = [IsAuthenticated]
```

Whe you try to access an endpoint, You will be restricted and you need a token to get it,

![no auth token request](./imgs/no-auth.png)

Acquire a token by going to the path **http://localhost:8000/auth/token**

![Get auth token](./imgs/get%20token.png)

Use the token to access the protected path

![Access path with token](./imgs/request%20with%20auth%20token.png)


## JWT Authentication

This is the type of Authentication where a server verifies a user using a JWT (JSON Web Token) pronounced **Jot**. JSON Web tokens are a small secure token that proves a user is authenticated. The client will send this token with every request to access protected resources.

### The structure of a JWT
A JWT contains 3 parts separated by dots. These include:

- **Header** : This contains the token metadata (like the algorithm, and type)
- **Payload**: This contains the data encoded into the token (claims like inf about a user)
- **Signature**: This verifies that the token is valid and has not been tampered with.

These will always be in such an order **header.payload.signature**

![a simple demo of a JWT](./imgs/example%20token.png)

For a client to obtain a JWT, they have to login to a server, which will verify the user making the request, and give them a token, clients store and then use the token on every request till it expires. The client will use the token in a request using the authorization header with the structure `Bearer <token>`

The server will always get the token in the request, verify it it is valid, checks expirationand extracts any data that may be important. 

### Implementing JWT Authentication with DRF

The most common way to implement JWT auth in DRF is to use a third party library called [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/). THis library covers most use cases when dealing with JWTs. To install it, run the command

```sh
pip install djangorestframework-simplejwt
```

After that, we need to configure the library to work with our project.    Firat we need to add its `JWTAuthentication` class to the `DEFAULT_AUTHENTICATION_CLASSES` list in the project level **settings.py**.