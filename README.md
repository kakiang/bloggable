# bloggable
A full-featured blog with Django

# Python web development with Django
I suppose you have python installed, as well as Django. If you don't have Django yet, just `pip install Django` at the shell prompt and you're good to go. If you do not also have Python installed, what are you waiting for? Go and do the work. 
## 1. Create a project
To create a project, run the following command  
```
$ django-admin startproject django_odyssey
```  
It creates a directory of the name of our django project. In this case it's __django_odyssey__. Inside that directory, we find:
- `manage.py` : This file is a command-line utility that will allow us to perform operations on our web app, such as creating apps, making migrations, running the development server, etc. We don't need to edit it.
- another directory with the name __django_odyssey__ and it contains
    - `__init__.py` : The presence of this file indicates that djangoproject is a python module or package. It is empty.
    - `settings.py` : This file contains all the settings of our web app, such as the database that we'll be using (SQLite by default), apps installed in our web app, etc. By default it contains initial basic settings that allows us to run a Django box out of the box.
    - `urls.py` : This file takes care of matching routes to views. In other words, it contains URL patterns for all the views of the web app. Though each app has its own `urls.py`, they have to be referenced in project's `urls.py` file. 
    - `wsgi.py` : It is a configuration file to run Django projects as Web Server Gateway Interface (WSGI) applications. Unless we're about to deploy our Django Web app in production, the default config works.

 ## 2. Create an app
 In order to avoid any confusion, let's define terms first.  What's a project in Django? And What's an app in Django?  

 __In Django, a project__ describes a Django web application defined primarily by a settings module. The project's root directory contains `manage.py` and all of the project's applications.  

 __An application in Django__ describes a Python package that interacts with various parts of the
framework and provides some specific functionalities to a project. It may be reused in
various projects. A Django app is practically some combination of models, views, templates, static files, and URLs. We can think of a Django project as our website which contains several
applications such as blog, wiki, or forum, which can be used in other projects.

So once the project is created, we then create apps. To create apps we have to do it from the project's root directory.

```
$ cd django_odyssey

$ python manage.py startapp blog
```
This generates a directory named __blog__ inside the project'root directory. The following is the structure and files inside a Django app directory.  

### 2.1 App structure
- `models.py` :
-  `views.py` : A Django view is a Python function that receives a web request and returns a web response. All the logic necessary to return the desired response is done inside the view. 
- `urls.py` :
- `admin.py` :
- `apps.py` :
- `tests.py` :
- `templates` :
    - `static files` :

