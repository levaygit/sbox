from django.urls import path

from .views import (
    ShopIndexView,
    ProductDetailsView,
    ProductsListView,
    ShopsListView,
    OrderDetailsView,
    PromotionDetailsView
)


app_name = "shop"

urlpatterns = [
    path('index/', ShopIndexView.as_view(), name='index'),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("shops/", ShopsListView.as_view(), name="shops"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("promotions/<int:pk>/", PromotionDetailsView.as_view(), name="promotion_details"),

]
