# Django Rest Framework (DRF) Course - Module 5
This is my DRF course. I hope you like it.

> These notes follow on from steps/module_4.md
***
***

## Current root directory
Your root directory should look like the following.
```
drf_course\  <--This is the root directory
    backend\
        core\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >serializers.py
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
        static\
        utils\
            >__init__.py
            >model_abstracts.py 
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
git checkout module_5
git pull origin module_5
```


## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

As I mentioned at the start of this course. This app will use token authentication to protect some of our endpoints. DRF makes this very easy.

Lets begin.

1) New app - We will apply token authentication on our ecommerce endpoints. However, we haven't created the app. Go ahead and create an ecommerce app with the following command.

```
python manage.py startapp ecommerce
```

2) Settings - Open /drf_course/settings.py and replace the REST_FRAMEWORK with the following code. Notice the new DEFAULT_AUTHENTICATION_CLASSES.

```
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
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

Now change INSTALLED_APPS to the following.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken', #Used to enable token authentication
    'core',
    'ecommerce', #New app
]
```
3) URL's - We now need to add a new endpoint to our urlconf file. Replace /drf_course/urls.py with the following code.

```
from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'contact', core_views.ContactViewSet, basename='contact')

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token), #gives us access to token auth
]
```

4) Migrate - You now need to migrate database changes. Use following code.
```
python manage.py makemigrations
python manage.py migrate
```

4) Signals - We need a mechanism to create a token for every user that signs up to our app. This token is what will be returned when we call the new endpoint. Go ahead and create a new file in /ecommerce and call it signals.py.
Use the following code in the new file.

```
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
```
Now open /ecommerce/app.py and add the following code.
```
from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        import ecommerce.signals
```


5) Create a user - Go ahead and create a new superuser. This will server 2 purposes. We we gain access to the built in Django admin page and we will also create a new token. Open a new terminal and use the following code.
```
python manage.py createsuperuser
```
Add a username, email and password.

6) Call the endpoint - You can call the new endpoint with the following commands. With any luck, you will receive a new token ID in the response.

The following commands will call the API end point:

>Note: change 'localhost' to 'api' if you make the calls via Docker Decktop.


```
curl -XPOST -F 'username=**your_username**' -F 'password=**your_password**' http://localhost:8000/api-token-auth/
```

```
http post http://localhost:8000/api-token-auth/ username=**your_username** password=**your_password**
```

These can both be used in the Docker CLI
```
curl -XPOST -F 'username=**your_username**' -F 'password=**your_password**' http://api:8000/api-token-auth/
```

```
http post http://api:8000/api-token-auth/ username=**your_username** password=**your_password**
```
With any luck, you should see something that looks like the following:

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Sun, 06 Nov 2022 21:59:20 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.10.8
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "token": "09790c70d0a1e1bc91853c14bbd320ec506af03b"
}
```

***
***

## Root directory
>Note: If all went well, your root directory should now look like this
```
drf_course\  <--This is the root directory
    backend\
        core\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >serializers.py
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
        ecommerce\ <-- New dir
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >signals.py <--New file
            >tests.py
            >views.py
        static\
        utils\
            >__init__.py
            >model_abstracts.py 
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
