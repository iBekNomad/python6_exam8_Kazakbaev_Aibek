from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, \
    UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView

from .base_views import SearchView
from webapp.models import Product
from ..forms import ProductForm


class IndexView(SearchView):
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 6
    paginate_orphans = 0
    model = Product
    search_fields = ['name__icontains', 'author__icontains']


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product
    paginate_reviews_by = 5
    paginate_reviews_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews, page, is_paginated = self.paginate_reviews(self.object)
        context['reviews'] = reviews
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_reviews(self, product):
        reviews = product.reviews.all().order_by('-rating')
        if reviews.count() > 0:
            paginator = Paginator(reviews, self.paginate_reviews_by, orphans=self.paginate_reviews_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return reviews, None, False


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.add_product'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'product/product_update.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    permission_required = 'webapp.delete_product'
    success_url = reverse_lazy('index')
