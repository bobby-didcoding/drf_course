# Django Rest Framework (DRF) Course - Module 2
This is my DRF course. I hope you like it.

> These notes follow on from steps/module_1.md
***
***

## Current root directory
Your root directory should look like the following.
```
drf_course\  <--This is the root directory
    backend\
        docker\
            ...
        drf_course\
            >__init__.py
            >asgi.py
            >settings.py
            >urls.py
            >wsgi.py
        >manage.py
        >requirements.txt
    steps\
        ...
    venv\
        include\
        Lib\
        Scripts\
    >.env
    >.gitignore
    >docker-compose.yml
    >env.template
    >README.md
    >server.py
```
If in doubt, run the following git commands:
```
git checkout module_2
git pull origin module_2
```

## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

"Django makes it easier to build better web apps more quickly and with less code."

In this module, we will be creating a Django application for our project. A Django application is a Python package that is specifically intended for use in a Django project. An application may use common Django conventions, such as having models, tests, urls, and views submodules. 

We will have 2 applications in our project:
The first will be core. This application will hold the logic for our contact us endpoint.
The second will be ecommerce. This app will hold the logic for our items and orders endpoints.
Lets go ahead and create the core application.

1) Applications - Open a terminal and use the following command to start a new application.
```
python manage.py startapp core
```

2) Settings - We need to spend some time in the Django settings file to get everything working. For instance, DRF has a bunch of specific settings we need tweak.

imports: Replace the current import section with the following snippet of code. It will give us access to our environment variables.

```
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()
```

variables: Replace ALLOWED_HOSTS, SECRET_KEY and DEBUG with the following snippet.
```
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
```

installed apps: Django will only know to include our new app in the project when we register it. Open drf_course/settings.py and register the new application in INSTALLED_APPS. Replace the current settings with the following snippet.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', #Great packaged to access abstract models
    'django_filters', #Used with DRF
    'rest_framework', #DRF package
    'core', # New app
]
```
DRF: We can now add the following variable to our project to access DRF features.

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

```

3) URL's - A clean, elegant URL scheme is an important detail in a high-quality web application. Django lets you design URLs however you want, with no framework limitations. To design URLs for an app, you create a Python module informally called a URLconf (URL configuration). This module is pure Python code and is a mapping between URL path expressions to Python functions (your views). Go ahead and open drf_course/urls.py (URLconf)and wire up the core application urls. Replace the code with the following snippet.

```
from django.urls import path
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
```

4) Migrations - Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations and when to run them. A new instance will always have a whole bunch of migrations waiting to be migrated. You can do this by running the following commands.

> Note: We are using the default db.sqlite3 database.
```
python manage.py makemigrations
python manage.py migrate
```

You should see this log similar to the following.
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

5) Local server - Django has a built in development server which is a lightweight web server written purely in Python. Django's development server allows us to develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production. Use the following command to start a local development server
```
python manage.py runserver
```

You should see this log.
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

November 05, 2022 - 12:18:44
Django version 4.1.3, using settings 'drf_course.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

You should now be up and running!
>Note: Open an incognito browser when testing your project (Ctrl + Shift + N)

* Our DRF course API interface is accessible at [http://localhost:8000](http://localhost:8000)

***
***

## Root directory
>Note: If all went well, your root directory should now look like this
```
drf_course\  <--This is the root directory
    backend\
        core\ <-- New core app
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >tests.py
            >views.py
        docker\
            ...
        drf_course\
            >__init__.py
            >asgi.py
            >settings.py
            >urls.py
            >wsgi.py
        >manage.py
        >requirements.txt
    steps\
        ...
    venv\
        include\
        Lib\
        Scripts\
    >.env
    >.gitignore
    >docker-compose.yml
    >env.template
    >README.md
    >server.py
```

***
***
