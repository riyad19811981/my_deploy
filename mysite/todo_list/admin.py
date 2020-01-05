from django.contrib import admin
from .models import Country, City, Category, Coin

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Coin)

