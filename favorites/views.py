
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from favorites.models import Favorites
from goods.models import Goods


@login_required
def fav_list(request):
    ads = Favorites.objects.filter(user=request.user)
    data = {'ads': ads}
    return render(request, 'favorites/fav_list.html', data)


@login_required
def fav_change(request, ad_id):
    product = Goods.objects.get(id=ad_id)
    favs = Favorites.objects.filter(user=request.user, product=product)
    if favs.exists():
        favs.delete()
        return JsonResponse({'is_favorite': False})
    else:
        Favorites.objects.create(user=request.user, product=product)
        return JsonResponse({'is_favorite': True})


