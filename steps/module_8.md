# Django Rest Framework (DRF) Course - Module 8
This is my DRF course. I hope you like it.

> These notes follow on from steps/module_7.md
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
        ecommerce\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >serilizers.py
            >signals.py
            >tests.py
            >views.py
        utils\
            >__init__.py
            >model_abstracts.py 
        >db.sqlite3
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
git checkout module_8
git pull origin module_8
```


## Steps/Commands

>Note: Please 'cd' into the root directory and fire up your virtual environment!

In the last 2 module, we built an 'item' and 'order' end point for users to purchase items. It seems to work okay but let's double down on testing.
In this module, we will write some unit tests to test our new endpoints.

DRF comes with a built in APIClient.

1) Unit tests - Copy the following code into /core/tests.py

```
from django.contrib.auth.models import User
from ecommerce.models import Item, Order
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class EcommerceTestCase(APITestCase):
    """
    Test suite for Items and Orders
    """
    def setUp(self):

        Item.objects.create(title= "Demo item 1",description= "This is a description for demo 1",price= 500,stock= 20)
        Item.objects.create(title= "Demo item 2",description= "This is a description for demo 2",price= 700,stock= 15)
        Item.objects.create(title= "Demo item 3",description= "This is a description for demo 3",price= 300,stock= 18)
        Item.objects.create(title= "Demo item 4",description= "This is a description for demo 4",price= 400,stock= 14)
        Item.objects.create(title= "Demo item 5",description= "This is a description for demo 5",price= 500,stock= 30)
        self.items = Item.objects.all()
        self.user = User.objects.create_user(
            username='testuser1', 
            password='this_is_a_test',
            email='testuser1@test.com'
        )
        Order.objects.create(item = Item.objects.first(), user = User.objects.first(), quantity=1)
        Order.objects.create(item = Item.objects.first(), user = User.objects.first(), quantity=2)
        
        #The app uses token authentication
        self.token = Token.objects.get(user = self.user)
        self.client = APIClient()
        
        #We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_get_all_items(self):
        '''
        test ItemsViewSet list method
        '''
        self.assertEqual(self.items.count(), 5)
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_item(self):
        '''
        test ItemsViewSet retrieve method
        '''
        for item in self.items:
            response = self.client.get(f'/item/{item.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_is_more_than_stock(self):
        '''
        test Item.check_stock when order.quantity > item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock + 1), False)

    def test_order_equals_stock(self):
        '''
        test Item.check_stock when order.quantity == item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock), True)

    def test_order_is_less_than_stock(self):
        '''
        test Item.check_stock when order.quantity < item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertTrue(i.check_stock(current_stock - 1), True)
    
    def test_create_order_with_more_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity > item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock+1)}
            response = self.client.post(f'/order/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_less_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity < item.stock
        '''
        for i in self.items:
            data = {"item": str(i.id), "quantity": 1}
            response = self.client.post(f'/order/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_with_equal_stock(self):
        '''
        test OrdersViewSet create method when order.quantity == item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock)}
            response = self.client.post(f'/order/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders(self):
        '''
        test OrdersViewSet list method
        '''
        self.assertEqual(Order.objects.count(), 2)
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_one_order(self):
        '''
        test OrdersViewSet retrieve method
        '''
        orders = Order.objects.filter(user = self.user)
        for o in orders:
            response = self.client.get(f'/order/{o.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
```

2) Run tests - You can run our new tests with the following command.
```
python manage.py test
```

With any luck, you should see the following in your terminal.
```
Found 18 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................
----------------------------------------------------------------------
Ran 18 tests in 2.436s

OK
Destroying test database for alias 'default'...
```

Let's make some calls to our new endpoint.

3) Call our endpoints - Here are the requests we can make to our new endpoints.

> This retrieves the auth token for **your_username**

curl -X POST -F 'username=**your_username**' -F 'password=**your_password**' http://api:8000/api-token-auth/

http post http://api:8000/api-token-auth/ username=**your_username** password=**your_password**


> This will retrieve all items

curl -X GET -H 'Authorization: Token **your_token**' http://api:8000/item/

http http://api:8000/item/ 'Authorization: Token **your_token**'


> This will retreive a single item

curl -X GET -H 'Authorization: Token **your_token**' http://api:8000/item/**your_item_uuid**/

http http://api:8000/item/**your_item_uuid**/ 'Authorization: Token **your_token**' 

> This retrieve all orders

curl -X GET -H 'Authorization: Token **your_token**' http://api:8000/order/

http http://api:8000/order/ 'Authorization: Token **your_token**'

> This will place an order for item id = **your_item_uuid** quantity = 1

curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Token **your_token**' -d '{"item": "**your_item_uuid**", "quantity": "1"}' http://api:8000/order/

http http://api:8000/order/ 'Authorization: Token **your_token**' item="**your_item_uuid**" quantity="1"


> This get order id = **your_order_uuid**

curl -X GET -H 'Authorization: Token **your_token**' http://api:8000/order/**your_order_uuid**/

http http://api:8000/order/**your_order_uuid**/ 'Authorization: Token **your_token**'

> This will create a contact request

curl -X POST -H "Content-type: application/json" -d '{"name": "Bobby Stearman", "message": "test", "email":"bobby@didcoding.com"}' 'http://api:8000/contact/'

http http://api:8000/contact/ name="Bobby Stearman" message="test" email="bobby@didcoding.com"

Congratulations!! You have a fully functioning and tested API!!

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
        ecommerce\
            __pycache__\
            migrations\
                >__init__.py
            >__init__.py
            >admin.py
            >apps.py
            >models.py
            >serilizers.py
            >signals.py
            >tests.py
            >views.py
        utils\
            >__init__.py
            >model_abstracts.py 
        >db.sqlite3
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
