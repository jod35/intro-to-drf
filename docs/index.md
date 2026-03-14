# Building APIs with the Django REST Framework

## What is the Django REST Framework?
The Django REST Framework is a powerful set of tools that enables developers to build APIs on top of the applications they build with Django. It helps developers expose the data and functionality of a Django web application to other applications over the internet.

Such apps include:

- web apps (built with JS frameworks)
- mobile apps
- desktop apps
- other APIs
- Third party integrations

Django by default offers responses as templates, but DRF simplifies responses by returning JSON—a format that can be consumed by many applications on many platforms.

## What django REST Framework provides

### **Serializers**
Serializers convert Python objects to formats understandable by other applications, e.g., JSON. 

![json from serializer ](./imgs/Screenshot%202026-03-08%20112242.png)

### **API Views**
We can implement both function-based and class-based views to handle common HTTP methods like:

- **GET**: Retrieve data
- **POST**: Create data 
- **PATCH**: Partially update data
- **PUT**: Update data
- **DELETE**: Remove data

### **Authentication**
DRF builds on top of the Django authentication application to implement common auth flows like:

- Session-based authentication
- Token authentication 
- JWT authentication

Authentication allows users to identify themselves so that they can get access to protected parts of an application.

### **Authorization**
DRF provides classes or mixins for controlling who gets access to what in an application.

For example:

- Only authenticated users can access a certain resource.
- Only users having a certain role can access or perform a certain action.

### **The browsable API**

You are often required to have an API client to test and document what your APIs do, but with DRF, there is an in-built browsable API—a tool that simplifies how you make requests to your API and how you document it. This is very useful during development.

### **Pagination, filtering, throttling**

- **Pagination**: Return results in pages
- **Filtering**: Helps you query data easily
- **Throttling**: Limits how many requests users can make    

## REST
DRF follows the architectural pattern known as [REST](https://en.wikipedia.org/wiki/REST)

REST stands for Representational State Transfer. In REST:

- resources are represented as URLs.
- HTTP methods point to actions on those resources

In our little product management API, 

| Method | Endpoint | Description |
|---|---|---|
| GET     | /api/v1/products |  Get all products |
| GET  | /api/v1/products/1 | Get a product by ID |
| POST  | /api/v1/products |  Create a product |
| PATCH | /api/v1/products/1  | Partially update a product |
| PUT | /api/v1/products/1 | Update a product | 
| DELETE | /api/v1/products/1  | Delete a product |