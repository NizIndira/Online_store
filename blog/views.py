from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'image',)
    extra_context = {
        'title': 'Dream shop - Blog',
        'sub_title': 'Add article'
    }

    def get_success_url(self):
        return reverse('blog:article', args=[self.object.pk])

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Увеличиваем счетчик просмотров
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        article_item = Article.objects.get(pk=self.kwargs.get('pk'))
        context_data['article_pk'] = article_item.pk
        context_data['title'] = f'{article_item.title}'

        return context_data


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'image', 'is_published')
    extra_context = {
        'title': 'Dream shop - Blog',
        'sub_title': 'Edit article'
    }

    def get_success_url(self):
        return reverse('blog:article', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context_data


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:articles')


class ArticleListView(ListView):
    model = Article
    extra_context = {
        'title': 'Dream shop - Blog',
        'sub_title': ''
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        # queryset = queryset.order_by('-created_at')
        return queryset