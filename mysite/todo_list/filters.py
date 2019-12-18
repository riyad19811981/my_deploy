from .models import Coin
import django_filters


class CoinFilter(django_filters.FilterSet):
    class Meta:
        model = Coin
        fields = '__all__'
