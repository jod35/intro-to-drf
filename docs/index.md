# Building APIs with the Django REST Framework

## What is the Django REST Framework?
The Django rest framework is a powerful set of tools that enables developers build APIs on top of the applications they build with Django. It helps developers expose data and functionality of a Django web application to other applications over the internet.

Such apps include:

- web apps (built with JS frameworks)
- mobile apps
- desktop apps
- other APIs
- Third party integrations

Django by default offers responses as templates but DRF simplifies rsponses by returning JSON, a format that can be consumed by may applications in many platforms.

## What django REST Framework provides

1. Serializers
Serializers convert python objects to formats understandable by applications i.e JSON. 

![json from serializer ](./imgs/Screenshot%202026-03-08%20112242.png)

2. API Views
We can implment both function based and class based views to handle common HTTP methods like

- **GET** : Retrieve data
- **POST**: Create data 
- **PATCH**: partially update data
- **PUT**: Update data
- **DELETE**: Remove data

3. Authentication
DRF build on top of the Django authentication application toimplement common auth flows like
- Session based authentication
- Token authentication 
- JWT authentication

Authentication allows users to identify themselves so that they can get access to protected parts of an application.

4. Authorization
   DRF provides classes or mixins for controlling who gets access to what in an application.
   Forexample:
    - Only authenticated users can access a certain resource
    - Only users having a certain role can access or perform a certain action

5. The browsable API
    You are always required to have an API client so you can test and document what your APIs do, But with DRF, there is an in-built browsable API. A tool that simplifies how you mke requests to your API and how you document it. Very useful in development.

6. Pagination , filtering, throttling
   - **Pagination**: Return results as pages
   - **Filtering**: Helps you query data easily
   - **Throttling**: Limits how many requests users make    

## REST
DRF follows the architectural pattern known as [REST](https://en.wikipedia.org/wiki/REST)

REST in full is Representation State Transfer. In REST, 
- resources are repreneted as URLs.
- HTTP methods point to actions on those resources

In our little product management API, 

| Method | endpoint | description |
|---|---|---|
| GET     | /api/v1/products |  get all products |
| GET  | /api/v1/products/1 | get all products |
| POST  | /api/v1/products |  get all products |
| PATCH | /api/v1/products/1  | partially update a product |
| PUT | /api/v1/products/1 | update a products | 
| DELETE | /api/v1/products/1  | delete a product |