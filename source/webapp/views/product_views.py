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
    paginate_by = 2
    paginate_orphans = 0
    model = Product
    search_fields = ['name__icontains', 'author__icontains']


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.add_product'


    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'product/product_update.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.change_product'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    permission_required = 'webapp.delete_product'
    success_url = reverse_lazy('index')
