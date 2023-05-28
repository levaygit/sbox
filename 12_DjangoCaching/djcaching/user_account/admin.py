from django.contrib import admin

from .views import Profile


@admin.register(Profile)
class OrderAdmin(admin.ModelAdmin):
    list_display = "user", "balance"
