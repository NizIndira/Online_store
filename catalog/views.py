from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Version


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator'] = self.request.user.groups.filter(name='Модератор').exists()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.groups.filter(name='Модератор').exists():
            form.fields['is_published'].widget = forms.HiddenInput()
        return form


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.created_by or self.request.user.groups.filter(name='Модератор').exists()

    def get_success_url(self):
        product = self.get_object()
        return reverse('catalog:product', kwargs={'pk': product.category.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.groups.filter(name='Модератор').exists():
            form.fields['is_published'].widget = forms.HiddenInput()
        return form


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product

    def get_success_url(self):
        product = self.get_object()
        return reverse('catalog:product', kwargs={'pk': product.category.pk})

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.created_by or self.request.user.groups.filter(name='Модератор').exists()
