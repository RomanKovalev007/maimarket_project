from django.shortcuts import render

from favorites.models import Favorites
from goods.models import Goods

# функция представления для отображения главной страницы
def main_page(request):
    ads = Goods.objects.filter(is_published=1)
    if request.user.is_authenticated:
        for ad in ads:
            if Favorites.objects.filter(user=request.user, product=ad).exists():
                ad.is_favorite = 'is-active'
            else:
                ad.is_favorite = ''
    data = {'ads': ads, 'title': 'Mai Market'}
    return render(request, 'main/index.html', data)

# функция представления для страницы поддержки
def support(request):
    data = {'title': 'Поддержка'}
    return render(request, 'main/support.html', data)

