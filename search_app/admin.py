from django.contrib import admin
from .models import Category, Product, Favorite, SearchHistory
from .models import Favorite


# モデルを管理画面に登録
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(SearchHistory)
