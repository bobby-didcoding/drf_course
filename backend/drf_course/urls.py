from django.urls import path
from django.contrib import admin
from core import views as core_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contact', core_views.ContactViewSet, basename='contact') #new endpoint for '/contact/'

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]