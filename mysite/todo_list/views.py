from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from .filters import CoinFilter
from .forms import CoinFilterForm, CoinPopupForm
from .models import Country, Category, Coin
from django.db.models import Sum, F, FloatField, Q
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from bootstrap_modal_forms.generic import (BSModalUpdateView, BSModalCreateView, BSModalReadView, BSModalDeleteView)


def in_guest_group(user):
    return user.groups.filter(name='Guest Group').exists()


def in_admin_group(user):
    return user.groups.filter(name='Admin Group').exists()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinsListJson(BaseDatatableView):
    # model = Coin

    def get_initial_queryset(self):
        category = self.request.GET.get('category', None)
        if category:
            if category == 'All Coins':
                qs = Coin.objects.annotate(row_number=Window(
                    expression=RowNumber(),
                    order_by=('country__name', 'realse_year_ad'))
                ).order_by('country__name', 'realse_year_ad')
            else:
                qs = Coin.objects.filter(category__name=category).annotate(row_number=Window(
                    expression=RowNumber(),
                    order_by=('country__name', 'realse_year_ad'))
                ).order_by('country__name', 'realse_year_ad')
        return qs

    def filter_queryset(self, qs):
        coin_search = self.request.GET.get('search[value]', None)

        if coin_search:
            q = Q(country__name__istartswith=coin_search)\
                | Q(currency_name__istartswith=coin_search)\
                | Q(realse_year_ad__istartswith=coin_search)\
                | Q(print_city__istartswith=coin_search)\
                | Q(quantity__istartswith=coin_search)\
                | Q(usa_price__istartswith=coin_search)\
                | Q(km__istartswith=coin_search)
            qs = qs.filter(q).order_by('country__name', 'realse_year_ad')
        return qs


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinsSearchJson(BaseDatatableView):
    model = Coin

    def get_initial_queryset(self):
        all_coins = Coin.objects.all().order_by('country__name', 'realse_year_ad')
        filter_coins = CoinFilter(self.request.GET, queryset=all_coins)
        return filter_coins.qs


@login_required
@user_passes_test(in_admin_group, login_url='denied')
def search(request):
    request.session[0] = 'search'
    countries = Country.objects.all
    categories = Category.objects.all
    isRequestEmpy = all(value == '' for value in request.GET.values())
    if isRequestEmpy:
        return render(request, 'search.html',
                      {'countries': countries, 'categories': categories, 'navbar': 'search'})
    else:
        form = CoinFilterForm(request.GET or None)
        if form.is_valid():
            filter_coins = getContext(form)
            return render(request, 'search.html',
                          {'filter_coins': filter_coins, 'countries': countries, 'categories': categories,
                           'context': filter_coins, 'navbar': 'search'})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinCreateView(BSModalCreateView):
    template_name = 'create_coin.html'
    form_class = CoinPopupForm
    success_message = 'Success: Coin was created.'

    def form_valid(self, form):
        form.save()
        return redirect('coins_list', category=self.request.session['0'])


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinReadView(BSModalReadView):
    model = Coin
    template_name = 'read_coin.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinDeleteView(BSModalDeleteView):
    model = Coin
    template_name = 'delete_coin.html'
    success_message = 'Success: Coin was deleted.'

    def get_success_url(self):
        if 'search' not in self.request.session['0']:
            return reverse('coins_list', kwargs={'category': self.request.session['0']})
        else:
            return reverse('search')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(in_admin_group, login_url='denied'), name='dispatch')
class CoinUpdateView(BSModalUpdateView):
    model = Coin
    template_name = 'update_coin.html'
    form_class = CoinPopupForm
    success_message = 'Success: Coin was updated.'

    def get_success_url(self):
        if 'search' not in self.request.session['0']:
            return reverse('coins_list', kwargs={'category': self.request.session['0']})
        else:
            return reverse('search')


@login_required
@user_passes_test(in_admin_group, login_url='denied')
def coins_list(request, category):
    request.session[0] = category
    return render(request, 'coins_list.html', {'category': category, 'navbar': category})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('user_login'))


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                if user.groups.filter(name='Guest Group').exists():
                    return HttpResponseRedirect(reverse('guest'))
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return render(request, 'login.html', {'login_error': 'Your account is not active'})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return render(request, 'login.html', {'login_error': 'Invalid login details supplied'})

    else:
        # Nothing has been provided for username or password.
        return render(request, 'login.html', {})


@login_required
@user_passes_test(in_admin_group, login_url='denied')
def home(request):
    return render(request, 'home.html', { 'navbar': 'home'})


@login_required
@user_passes_test(in_guest_group, login_url='denied/')
def guest(request):
    all_coins = Coin.objects.all().order_by('country__name', 'realse_year_ad')
    return render(request, 'guest.html', {'all_coins': all_coins})


def denied(request):
    return HttpResponse("Access Denied")


@login_required
@user_passes_test(in_admin_group, login_url='denied')
def summary(request):
    total_quantity = Coin.objects.aggregate(Sum('quantity'))

    usa_total_price = Coin.objects.aggregate(value=Sum(F('quantity') * F('usa_price'), output_field=FloatField()))

    ksa_total_price = usa_total_price['value'] * 3.75

    total_quantity_by_category = Coin.objects.values('category__name').annotate(Sum('quantity')) \
        .annotate(usa_value=Sum(F('quantity') * F('usa_price'), output_field=FloatField())) \
        .annotate(ksa_value=Sum(F('quantity') * F('usa_price') * 3.75, output_field=FloatField()))

    total_quantity_by_country = Coin.objects.values('country__name').annotate(Sum('quantity')) \
        .annotate(usa_value=Sum(F('quantity') * F('usa_price'), output_field=FloatField())) \
        .annotate(ksa_value=Sum(F('quantity') * F('usa_price') * 3.75, output_field=FloatField()))

    return render(request, 'summary.html',
                  {'total_quantity_by_country': total_quantity_by_country, 'usa_total_price': usa_total_price,
                   'total_quantity_by_category': total_quantity_by_category,
                   'total_quantity': total_quantity,
                   'ksa_total_price': ksa_total_price, 'navbar': 'summary'})


@login_required
@user_passes_test(in_admin_group, login_url='denied')
def about(request):
    context = {'first_name': 'Salah', 'last_name': 'Alkhatib', 'greeting': 'hello world'}
    return render(request, 'about.html', context)


def getContext(form):
    country = form.cleaned_data.get("country")
    category = form.cleaned_data.get("category")
    currency_name = form.cleaned_data.get("currency_name")
    currency_value = form.cleaned_data.get("currency_value")
    realse_year_ad = form.cleaned_data.get("realse_year_ad")
    realse_year_ah = form.cleaned_data.get("realse_year_ah")
    km = form.cleaned_data.get("km")
    metal_type = form.cleaned_data.get("metal_type")
    quantity = form.cleaned_data.get("quantity")
    usa_price = form.cleaned_data.get("usa_price")
    catalog_price = form.cleaned_data.get("catalog_price")
    pick_number = form.cleaned_data.get("pick_number")
    serial_number = form.cleaned_data.get("serial_number")
    remarks = form.cleaned_data.get("remarks")
    print_city = form.cleaned_data.get("print_city")
    return {'currency_name': currency_name, 'realse_year_ad': realse_year_ad,
            'realse_year_ah': realse_year_ah, 'km': km, 'metal_type': metal_type,
            'quantity': quantity, 'usa_price': usa_price, 'catalog_price': catalog_price,
            'pick_number': pick_number, 'serial_number': serial_number, 'print_city': print_city,
            'country': country, 'category': category, 'remarks': remarks, 'currency_value': currency_value}




