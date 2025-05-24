from django.shortcuts import render

from goods.models import Goods

# функция представления для отображения главной страницы
def main_page(request):
    ads = Goods.objects.filter(is_published=1)
    data = {'ads': ads, 'title': 'Mai Market'}
    return render(request, 'main/index.html', data)

# функция представления для страницы поддержки
def support(request):
    data = {'title': 'Поддержка'}
    return render(request, 'main/support.html', data)

