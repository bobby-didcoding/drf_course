# Django Rest Framework (DRF) Course - Module 4
This is my DRF course. I hope you like it.

> These notes follow on from steps/module_3.md
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
git checkout module_4
git pull origin module_4
```

## Steps/Commands
>Note: Please 'cd' into the root directory and fire up your virtual environment!

In the last module, we built a '/contact/' end point for uses to get in touch with us. It seems to work okay but let's double down on testing.
In this module, we will write some unit tests to test our new endpoint.

DRF comes with a built in APIClient to 

1) Unit tests - Copy the following code into /core/tests.py
```
from . models import Contact
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status



class ContactTestCase(APITestCase):

    """
    Test suite for Contact
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "Billy Smith",
            "message": "This is a test message",
            "email": "billysmith@test.com"
        }
        self.url = "/contact/"

    def test_create_contact(self):
        '''
        test ContactViewSet create method
        '''
        data = self.data
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().title, "Billy Smith")

    def test_create_contact_without_name(self):
        '''
        test ContactViewSet create method when name is not in data
        '''
        data = self.data
        data.pop("name")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_contact_when_name_equals_blank(self):
        '''
        test ContactViewSet create method when name is blank
        '''
        data = self.data
        data["name"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_message(self):
        '''
        test ContactViewSet create method when message is not in data
        '''
        data = self.data
        data.pop("message")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_contact_when_message_equals_blank(self):
        '''
        test ContactViewSet create method when message is blank
        '''
        data = self.data
        data["message"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_without_email(self):
        '''
        test ContactViewSet create method when email is not in data
        '''
        data = self.data
        data.pop("email")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_contact_when_email_equals_blank(self):
        '''
        test ContactViewSet create method when email is blank
        '''
        data = self.data
        data["email"] = ""
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_when_email_equals_non_email(self):
        '''
        test ContactViewSet create method when email is not email
        '''
        data = self.data
        data["email"] = "test"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

2) Run tests - Go ahead and run our new tests.

```
python manage.py test
```

3) Call API - We're ready to call the 'contact' endpoint. I like to user (Curl)[https://curl.se/] or (Httpie)[https://httpie.io/].

You'll need to fire up Docker if you've decdied to go down the docker route. If this is the case, use the following command.
```
docker-compose up -d --build
```
Now open a cli in the 'drf_course_api' container...You're now ready to us the following commands.

>Note: Change 'localhost' to 'api' if you are using docker
```
curl -XPOST -H "Content-type: application/json" -d '{"name": "Bobby Stearman", "message": "test", "email":"bobby@didcoding.com"}' 'http://localhost:8000/contact/'
```

```
http post http://localhost:8000/contact/ name='Bobby Stearman' message='This is a test' email=bobby@didcoding.com
```


4) Check database - You can now use the Django shell to check the database for our new contact entry. Open Django shell with the following command.
```
python manage.py shell
```
Now use the following command and check the database for our new entry
```
from core.models import Contact
c = Contact.objects.latest(created)
c.title
```

Perfect - Everything is working as expected
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