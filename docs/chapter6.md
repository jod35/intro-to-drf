# Pagination, Filtering, and Throttling

Django REST Framework (DRF) provides robust built-in support for pagination, allowing you to manage large datasets efficiently by serving data in smaller chunks.

## Pagination

Pagination divides a large result set into discrete pages, improving performance and user experience through "previous" and "next" navigation links.

> **Note:** Ensure you have seeded your database with sufficient data to test these pagination features.

### Limit-Offset Pagination

Limit-offset pagination mimics SQL syntax, allowing clients to specify:

- **Limit**: The maximum number of items to return in a single request.
- **Offset**: The starting index from which to begin retrieving items.

To enable this globally, update your `settings.py` file:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10
}
```

This configuration automatically structures your list endpoint responses to include navigation metadata:

![Limit offset pagination](./imgs/limitoffset%20pagination.png)

### Page Number Pagination

This is the most common pagination style, where data is requested by a specific page number.

To enable it globally, modify your `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

If you want to allow clients to dynamically set the page size using a query parameter (e.g., `?page_size=20`), add the `PAGE_SIZE_QUERY_PARAM` setting:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "PAGE_SIZE_QUERY_PARAM": "page_size",
}
```

![page number pagination](./imgs/page%20number%20pagination.png)


## Filtering

### Basic Filtering with Querysets
DRF's list views by default will return all items but you can modify their behavior overriding the `get_queryset` method of the view class.

```py

# products/views.py
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Product.objects.filter(
            # add your filters here
        )
```

For example we can filter our products based on their names using query parameters.

```py
# products/views.py
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        query = Product.objects.all()

        name = self.request.GET.get('name')
        if name is not None:
            query = query.filter(name__icontains = name)
        return query
```

That will filter our products to list those with a name that is the same as what we provide in the query param.

### Complex Filters with Django-Filter
For more advanced filtering, we can employ the **Django-Filter** package. To set it up we can install it with

```sh
pip install django-filter
```

Then we can add it to our installed apps

```sh
INSTALLED_APPS = [
    # ... more apps here
    # third party apps
    "rest_framework",
    "django_filters"
]
```

Finally in our views,

```py

# products/views.py
# ... more imports here
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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return super().get_serializer_class()

```

With such a setup, you can be able to perform much more complex filtering like `http://127.0.0.1:8000/products/?name=toyota&max_price=120000`