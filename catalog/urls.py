from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, CategoryListView, CategoryDetailView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/category/', CategoryDetailView.as_view(), name='category'),
    path('<int:pk>/product/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create', ProductCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name='delete'),
]