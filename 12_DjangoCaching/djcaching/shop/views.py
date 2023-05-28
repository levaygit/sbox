from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

from .models import Product, Shop, Promotion, Order


class ShopIndexView(TemplateView):
    template_name = 'shop/index.html'


class ProductDetailsView(DetailView):
    template_name = "shop/product-details.html"
    model = Product
    context_object_name = "product"


class OrderDetailsView(UserPassesTestMixin, DetailView):
    def test_func(self):
        order = Order.objects.select_related('user').get(pk=self.kwargs['pk'])
        return (self.request.user.is_superuser or
                self.request.user.pk == order.user.pk)

    template_name = "shop/order-details.html"
    queryset = (
        Order.objects
        .prefetch_related("products")
    )
    context_object_name = "order"


class PromotionDetailsView(UserPassesTestMixin, DetailView):

    def test_func(self):
        if self.request.user.is_authenticated:
            promotions = Promotion.objects.filter(Q(users__in=[self.request.user.pk]) | Q(users__isnull=True))
            return (self.request.user.is_superuser or
                    self.kwargs['pk'] in promotions.values_list('pk', flat=True))
        else:
            return False

    template_name = "shop/promotion-details.html"
    queryset = (
        Promotion.objects
        .prefetch_related("products")
    )
    context_object_name = "promotion"


class ProductsListView(ListView):
    template_name = "shop/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ShopsListView(ListView):
    template_name = "shop/shops-list.html"
    model = Shop
    context_object_name = "shops"



