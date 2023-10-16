from django.shortcuts import render

from catalog.models import Category, Product


def home(request):
    category_list = Category.objects.all()
    context = {
        'object_list': category_list
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} {phone} {message}")
    return render(request, 'catalog/contacts.html')

def category(request, pk):
    context = {
        'object_list': Product.objects.filter(category_id=pk)
    }
    return render(request, 'catalog/category.html', context)


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'object': product_item,
        'title': f'{product_item.name}',
        'sub_title': ''
    }
    return render(request, 'catalog/product.html', context)