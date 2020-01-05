from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Coin(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency_name = models.CharField(max_length=50)
    currency_value = models.CharField(max_length=50)
    realse_year_ad = models.CharField(max_length=50)
    realse_year_ah = models.CharField(max_length=50)
    km = models.CharField(max_length=50, null=True, blank=True)
    metal_type = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField()
    usa_price = models.FloatField()
    catalog_price = models.FloatField(null=True, blank=True)
    pick_number = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    print_city = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.currency_name

    @property
    def usa_total_price(self):
        number = round(self.quantity * self.usa_price, 2)
        # to to return number with comma seperator
        return "{:,}".format(number)

    @property
    def sar_total_price(self):
        number = round(self.quantity * self.usa_price * 3.75, 2)
        # to to return number with comma seperator
        return "{:,}".format(number)


