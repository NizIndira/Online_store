from django.shortcuts import render
from django.views.generic import ListView, DetailView

from catalog.models import Category, Product

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/home.html'


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} {phone} {message}")
    return render(request, 'catalog/contacts.html')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.filter(category_id=self.kwargs.get('pk'))
        return context_data
