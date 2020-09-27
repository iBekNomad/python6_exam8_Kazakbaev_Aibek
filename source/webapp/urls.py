from django.urls import path, include

from webapp.views import IndexView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ReviewUpdateView, ReviewDeleteView, ReviewCreateView, review_mass_action_view, ReviewView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('product/', include([
        path('<int:pk>/', ProductView.as_view(), name='product_view'),
        path('add/', ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
        path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
        path('<int:pk>/reviews/add/', ReviewCreateView.as_view(), name='review_create')
    ])),
    path('review/', include([
        path('<int:pk>/', include([
            path('', ReviewView.as_view(), name='review_view'),
            path('update/', ReviewUpdateView.as_view(), name='review_update'),
            path('delete/', ReviewDeleteView.as_view(), name='review_delete'),
        ])),
        path('mass-action/', review_mass_action_view, name='review_mass_action'),
    ]))
]
