import datetime

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Order, Product, Shop, Promotion


class ComplexShopViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='test_client',
            password='qwerty',
        )
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='ul. Sergeeva, h. 12',
            promocode='FOOBAR',
            user=self.user,
        )

        self.product = Product.objects.create(
            name='test_product',
            description='test_product_decription',
            price=100,
            discount=0,
        )

        self.shop = Shop.objects.create(
            name='test_shop',
            address='address_test_shop',
            opening=datetime.time(8, 0),
            closing=datetime.time(18, 0),
        )

        self.promotion = Promotion.objects.create(
            name='test_promotion',
            description='test_promotion_description',
            start=datetime.date.today(),
            end=datetime.date(2023, 12, 12),
        )

        self.order.products.add(self.product)
        self.order.save()

    def tearDown(self) -> None:
        Order.objects.filter(user=self.user).delete()

    def test_order_details(self):
        response = self.client.get(
            reverse('shop:order_details', kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, 'Promocode: FOOBAR')
        self.assertContains(response, 'Delivery address: ul. Sergeeva, h. 12')
        self.assertContains(response, self.product.name)

    def test_products_list(self):
        response = self.client.get(
            reverse('shop:products_list')
        )
        self.assertContains(response, self.product.name)

    def test_shops_list(self):
        response = self.client.get(
            reverse('shop:shops')
        )
        self.assertContains(response, self.shop.name)
        self.assertContains(response, self.shop.address)

    def test_orders_list_in_user_accounts(self):
        response = self.client.get(
            reverse('user_account:about_me', kwargs={'pk': self.user.pk})
        )
        self.assertContains(response, self.order.pk)
        self.assertContains(response, self.order.delivery_address)

    def test_promotions_list_in_user_accounts(self):
        response = self.client.get(
            reverse('user_account:about_me', kwargs={'pk': self.user.pk})
        )
        self.assertContains(response, 'test_promotion')

    def test_promotion_details(self):
        response = self.client.get(
            reverse('shop:promotion_details', kwargs={'pk': self.promotion.pk})
        )
        self.assertContains(response, 'test_promotion')
        self.assertContains(response, 'test_promotion_description')



