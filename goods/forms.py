from django import forms
from goods.models import Goods, Categories, Address, Condition


class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label='Категория не выбрана',
                                      label='Категория', required=True,
                                      widget=forms.Select(attrs={'class': "add-product__categori-input"}))
    address = forms.ModelChoiceField(queryset=Address.objects.all(), empty_label='Адрес не выбран',
                                      label='Местоположение', required=True,
                                      widget=forms.Select(attrs={'class': "add-product__categori-input"}))
    condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label='Состояние не выбрано',
                                     label='Состояние', required=True,
                                     widget=forms.Select(attrs={'class': "add-product__categori-input"}))

    image = forms.ImageField(required=True,
        widget=forms.FileInput(
        attrs={'class': "add-product__upload-input", 'hidden': True, 'id': "fileInput", 'accept': "image/*"}))

    class Meta:
        model = Goods
        fields = ['name','image', 'category', 'address', 'condition', 'description', 'price']

        labels = {
            'name': 'Название товара',
            'image': 'Фотографии',
            'category': 'Категория',
            'description': 'Описание',
            'price': 'Цена',
        }

        # cостояние бу/новое
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название', 'class': "add-product__name-input"}),
            'description': forms.Textarea(attrs={'placeholder': 'Опишите ваш товар или услугу', 'class': "add-product__area"}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите цену', 'class': "add-product__price-input"}),
        }


class GoodsFilterForm(forms.Form):
    query = forms.CharField(
        label='Поиск по названию',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название', 'class' :"product-filters__query-input"})
    )
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        label='Категория',
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={'class': "product-filters__categories-input"})
        #  name="catrgories" id="choseCategori"
    )
    min_price = forms.IntegerField(
        label='Минимальная цена',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'От', 'class' : "product-filters__price-input"})
        #  id="priceMin" name="minimumPrice"
    )
    max_price = forms.IntegerField(
        label='Максимальная цена',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'До', 'class' : "product-filters__price-input"})
    )
    address = forms.ModelChoiceField(
        queryset=Address.objects.all(),
        label='Местоположение',
        required=False,
        empty_label='Не указано',
        widget=forms.Select(attrs={'class': "product-filters__categories-input"})
    )
