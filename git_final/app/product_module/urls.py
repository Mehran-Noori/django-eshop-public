from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_list_by_brands'),

    # path('u', views.ProductDetailView.as_view(), name='product_detail'),
    # path('', views.AddProductReview.as_view(), name='add_product_review'),
]
