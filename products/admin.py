from django.contrib import admin
from products.models import Product, Category, SearchWord, Review

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SearchWord)
admin.site.register(Review)
