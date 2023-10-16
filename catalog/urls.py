from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, category, product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/category/', category, name='category'),
    path('<int:pk>/product/', product, name='product')
]