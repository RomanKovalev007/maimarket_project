from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.db.models import Q
from goods.forms import AdForm, GoodsFilterForm
from goods.models import Goods


class AddAd(LoginRequiredMixin, CreateView):
    form_class =  AdForm
    template_name = 'goods/add_ad.html'
    extra_context = {'title': 'Новое объявление'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        w = form.save(commit=False)
        w.seller = self.request.user
        return super().form_valid(form)


def goods_list(request):
    form = GoodsFilterForm(request.GET or None)
    ads = Goods.objects.filter(is_published=True)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        address = form.cleaned_data.get('address')

        if query:
            ads = ads.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        if category:
            ads = ads.filter(category=category)

        if min_price is not None:
            ads = ads.filter(price__gte=min_price)

        if max_price is not None:
            ads = ads.filter(price__lte=max_price)

        if address is not None:
            ads = ads.filter(address=address)


    context = {
        'ads': ads,
        'title': 'Лента объявлений',
        'form': form
    }
    return render(request, 'goods/goods_list.html', context)


def show_ad(request, ad_slug):
    ad = get_object_or_404(Goods, slug=ad_slug)
    context = {
        'ad': ad,
        'title': ad.name
    }
    return render(request, 'goods/product-card.html', context)


def edit_ad(request, ad_slug):
    ad = get_object_or_404(Goods, slug=ad_slug)

    if request.user != ad.seller:
        raise PermissionDenied("У вас нет прав для редактирования этого объявления")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            updated_ad = form.save()
            return redirect('goods:ad', ad_slug=updated_ad.slug)
    else:
        form = AdForm(instance=ad)

    context = {
        'form': form,
        'ad': ad,
        'title': 'Редактирование объявления'
    }
    return render(request, 'goods/add_ad.html', context)

def remove_ad(request, ad_slug):
    ad = Goods.objects.get(slug=ad_slug)
    if ad.is_published:
        ad.is_published = False
        ad.save()
    else:
        ad.is_published = True
        ad.save()
    return redirect(request.META['HTTP_REFERER'])
