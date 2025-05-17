from django.contrib import admin

from goods.models import Categories, Goods, Address, Condition


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}