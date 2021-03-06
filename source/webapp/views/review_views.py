from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import  get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView
from webapp.forms import ProductForm, ReviewForm
from webapp.models import Review, Product


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/review_create.html'
    form_class = ReviewForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.product = product
        review.author = self.request.user
        review.save()
        return redirect('webapp:product_view', pk=product.pk)


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/review_update.html'
    form_class = ReviewForm
    permission_required = 'webapp.change_review'

    def has_permission(self):
        review = self.get_object()
        return super().has_permission() or review.author == self.request.user

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})


class ReviewDeleteView(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    permission_required = 'webapp.delete_review'

    def test_func(self):
        review = Review.objects.get(pk=self.kwargs.get('pk'))
        return self.request.user == review.author or self.request.user.has_perm('webapp.delete_review')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})


class ReviewView(DetailView):
    template_name = 'review/review_view.html'
    model = Review
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def review_mass_action_view(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_reviews', [])
        if 'delete' in request.POST:
            Review.objects.filter(id__in=ids).delete()
    return redirect('webapp:index')
