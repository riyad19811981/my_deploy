from .models import Coin
import django_filters


class CoinFilter(django_filters.FilterSet):
    remarks = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Coin
        fields = '__all__'
