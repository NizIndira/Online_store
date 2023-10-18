from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, CategoryListView, CategoryDetailView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/category/', CategoryDetailView.as_view(), name='category'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product')
]