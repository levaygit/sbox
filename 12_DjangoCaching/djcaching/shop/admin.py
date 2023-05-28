from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


from .models import Product, Order, Shop, Promotion


@admin.action(description=_("Archive products"))
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description=_("Unarchive products"))
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
    ]

    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
           "fields": ("name", "description"),
        }),
        (_("Price options"), {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        (_("Extra options"), {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": _("Extra options. Field 'archived' is for soft delete"),
        })
    ]

    @admin.display(description=_('description_short'))
    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class OrderProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductInline
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"
    fieldsets = [
        (None, {
           "fields": ("delivery_address", "promocode", "user"),
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = "name", "address", "opening", "closing"


class PromotionProductInline(admin.StackedInline):
    model = Promotion.products.through


class PromotionUserInline(admin.StackedInline):
    model = Promotion.users.through


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    inlines = [
        PromotionProductInline,
        PromotionUserInline
    ]
    list_display = "name", "description_short", "start", "end",

    fieldsets = [
        (None, {
           "fields": ("name", "description", "start", "end"),
        }),
    ]

    def get_queryset(self, request):
        return Promotion.objects.prefetch_related("products", "users")

    def user_verbose(self, obj: Promotion) -> str:
        return obj.user.first_name or obj.user.username

    @admin.display(description=_('description_short'))
    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."
