from django.urls import path
from .views import CategoryList, CategoryDetails


urlpatterns = [
    path('category/list/', CategoryList, name='Category_List'),
    path('category/details/', CategoryDetails, name='Category_Details'),
]