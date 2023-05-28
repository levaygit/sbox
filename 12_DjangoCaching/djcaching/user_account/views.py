from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import reverse, render
from django.views.generic import CreateView, View
from django.db.models import Q
from django.core.cache import cache

from .models import Profile
from shop.models import Order, Promotion


class AboutMeView(UserPassesTestMixin, View):
    def test_func(self):
        return (self.request.user.is_superuser or
                self.request.user.pk == self.kwargs['pk'])

    def get(self, request: HttpRequest, pk):
        user = User.objects.select_related('profile').get(pk=pk)
        order = Order.objects.filter(user=pk)

        promotions_cache_key = 'promotions: {}'.format(user.username)
        promotions = Promotion.objects.filter(Q(users__in=[pk]) | Q(users__isnull=True))
        cache.get_or_set(promotions_cache_key, promotions, 30*60)

        context = {
            'object': user,
            'orders': order,
            'promotions': promotions,
        }
        return render(request, "user_account/about-me.html", context=context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "user_account/register.html"

    def get_success_url(self):
        return reverse('shop:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("user_account:login")
