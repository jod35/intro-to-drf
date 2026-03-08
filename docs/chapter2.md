# Building a CRUD API
Now that we have built the foundation, let us get our hands dirty and build a simple CRUD REST API with DRF.

## Project Set Up
We have to create an environment in which our dependencies will be install in isolation from our Python installtion systemwide, you can use **venv** with PIP in the following way.

### Create a new empty folder
Let us begin by creating a new folder any where we prefer on our file-system , call it `product-inventory`

### Create a vitual environment 
Creating  a virtual environment with venve is going to be done using the following command.

```sh
c:\Users\jod35\product-inventory> python -m venv env
```

This will create a new folder called **env** in your project folder. 

### Activate the environment
Activate the environment with the following command.

On Windows,
```sh
c:\Users\jod35\product-inventory> env\Scripts\activate # Windows
```
On Linux Based System,
```sh
$ source env/bin/activate # Linux / Unix-based system 
```

With your virtualenv set up, you should now be ready to install Django. 

### Installing Django and Django REST Framework
We will use PIP to do this through the command
```
pip install djangorestframework
```

To keep track of our necessary dependencies for the project, we are going to create a special **requirements.txt** file which will be used to install project dependencies if we are to deploy or ditribute our code to other developers.

```
pip freeze > requirements.txt
```
The above command gets the ouput of the `pip freeze` and writes it to the file **requirements.txt** allowing you to create a reproducible list of dependencies ith their exact versions

### Creating a Django Project
