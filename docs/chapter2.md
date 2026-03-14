# Building a CRUD API
Now that we have built the foundation, let's build a simple CRUD REST API with Django REST Framework (DRF).

## Project Setup
We need to create an isolated environment for our dependencies using **venv** and PIP.

### Create a new empty folder
Create a new folder anywhere on your file system and name it `product-inventory`.

### Create a virtual environment
Create a virtual environment using the following command:

```sh
python -m venv env
```

This creates a new folder called **env** in your project directory.

### Activate the environment
Activate the environment with the appropriate command for your operating system.

On Windows:
```sh
env\Scripts\activate
```

On Linux or Unix-based systems:
```sh
$ source env/bin/activate
```

With your virtual environment active, you're ready to install Django.

### Install Django and Django REST Framework
Use PIP to install the required packages:

```
pip install djangorestframework
```

Create a **requirements.txt** file to track dependencies for deployment or sharing with other developers:

```
pip freeze > requirements.txt
```

This command captures all installed packages and their versions in **requirements.txt**.

### Create a Django Project
The Django installation provides the `django-admin` command. Use it to create a new project:

```sh
django-admin startproject core .
```

The `django-admin` command is Django's CLI utility for managing tasks. The `startproject` subcommand creates boilerplate code to get started.

This command creates a **core** folder and a **manage.py** file. The **core** folder contains Django project settings and configurations, while **manage.py** is used to manage your Django application going forward.

### Run the server
Start the development server:

```sh
python manage.py runserver
```

This starts a development server at **http://localhost:8000**.

![Django installation successful](./imgs/hello%20world.png)