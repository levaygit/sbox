from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        return HttpResponseRedirect(reverse('shop:index'))
