from django.urls import path
from .views import CategoryList, CategoryDetails, ServiceList, ServiceDetails


urlpatterns = [
    path('category/list/', CategoryList, name='Category_List'),
    path('category/details/', CategoryDetails, name='Category_Details'),
    path('service/list/', ServiceList, name='Service_List'),
    path('service/details/', ServiceDetails, name='Service_Details'),
]