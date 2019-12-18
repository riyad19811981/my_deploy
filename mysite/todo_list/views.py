from django.contrib import messages
from django.shortcuts import render, redirect

from .filters import CoinFilter
from .forms import ListForm, MyDjangoForm, UserForm, UserProfileInfoForm, CoinFilterForm, CoinForm
from .models import List, Country, Category, Coin
from django.views.generic import View
from django.db.models import Q, Sum, F, FloatField

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class CBView(View):
    def get(self, request):
        return HttpResponse('Class based view is cool!')


def hello(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("Hello World!")


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")


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
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'login.html', {})


def show_image(request):
    return render(request, 'show_image.html')


def home(request):
    all_coins = Coin.objects.all().order_by('country__name', 'realse_year_ad')
    return render(request, 'home.html', {'all_coins': all_coins, 'navbar': 'home'})


def coins(request, category):
    all_coins = Coin.objects.filter(category__name=category).order_by('country__name', 'realse_year_ad')
    return render(request, 'home.html', {'all_coins': all_coins, 'navbar': category})


def summary(request):
    total_quantity = Coin.objects.aggregate(Sum('quantity'))

    usa_total_price = Coin.objects.aggregate(value=Sum(F('quantity') * F('usa_price'), output_field=FloatField()))

    ksa_total_price = usa_total_price['value'] * 3.75

    # total_quantity_by_category = Coin.objects.values('category__name').annotate(Sum('quantity'))

    total_quantity_by_category = Coin.objects.values('category__name').annotate(Sum('quantity')).annotate(value=Sum(F('quantity') * F('usa_price'), output_field=FloatField()))

    total_quantity_by_country = Coin.objects.values('country__name').annotate(Sum('quantity')).annotate(value=Sum(F('quantity') * F('usa_price'), output_field=FloatField()))

    return render(request, 'summary.html',
                  {'total_quantity_by_country': total_quantity_by_country, 'usa_total_price': usa_total_price,
                   'total_quantity_by_category': total_quantity_by_category,
                   'total_quantity': total_quantity,
                   'ksa_total_price': ksa_total_price, 'navbar': 'summary'})


def search(request):
    countries = Country.objects.all
    categories = Category.objects.all
    isRequestEmpy = all(value == '' for value in request.GET.values())
    if isRequestEmpy:
        return render(request, 'search.html',
                      {'countries': countries, 'categories': categories, 'navbar': 'search'})
    else:
        form = CoinFilterForm(request.GET or None)
        if form.is_valid():
            context = getContext(form)
            coins_list = Coin.objects.all().order_by('country__name', 'realse_year_ad')
            filter_coins = CoinFilter(request.GET, queryset=coins_list)
            return render(request, 'search.html',
                          {'filter_coins': filter_coins, 'countries': countries, 'categories': categories,
                           'context': context, 'navbar': 'search'})


def about(request):
    context = {'first_name': 'Salah', 'last_name': 'Alkhatib', 'greeting': 'hello world'}
    return render(request, 'about.html', context)


def getContext(form):
    country = form.cleaned_data.get("country")
    category = form.cleaned_data.get("category")
    currency_name = form.cleaned_data.get("currency_name")
    realse_year_ad = form.cleaned_data.get("realse_year_ad")
    realse_year_ah = form.cleaned_data.get("realse_year_ah")
    km = form.cleaned_data.get("km")
    metal_type = form.cleaned_data.get("metal_type")
    quantity = form.cleaned_data.get("quantity")
    usa_price = form.cleaned_data.get("usa_price")
    catalog_price = form.cleaned_data.get("catalog_price")
    pick_number = form.cleaned_data.get("pick_number")
    serial_number = form.cleaned_data.get("serial_number")
    return {'currency_name': currency_name, 'realse_year_ad': realse_year_ad,
            'realse_year_ah': realse_year_ah, 'km': km, 'metal_type': metal_type,
            'quantity': quantity, 'usa_price': usa_price, 'catalog_price': catalog_price,
            'pick_number': pick_number, 'serial_number': serial_number,
            'country': country, 'category': category}


def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request, 'Item has been deleted')
    return redirect('home')


def deletecoin(request, coin_id):
    item = Coin.objects.get(pk=coin_id)
    item.delete()
    messages.success(request, 'Item has been deleted')
    return redirect('home')


def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')


def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')


def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been edited')
            return redirect('home')

    else:
        item = List.objects.get(pk=list_id)
        return render(request, 'edit.html', {'item': item})


def addcoin(request):
    if request.method == 'POST':
        form = CoinForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been added')
            return redirect('home')
    else:
        form = CoinForm()
        return render(request, 'editcoin.html', {'form': form, 'coin_id': 0, 'disable_delete': 'hidden'})


def editcoin(request, coin_id):
    countries = Country.objects.all
    categories = Category.objects.all
    if request.method == 'POST':
        item = Coin.objects.get(pk=coin_id)
        form = CoinForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been edited')
            return redirect('home')

    else:
        item = Coin.objects.get(pk=coin_id)
        form = CoinForm(request.POST or None, instance=item)
        return render(request, 'editcoin.html',
                      {'form': form, 'coin_id': coin_id, 'countries': countries, 'categories': categories})


def my_django_form(request):
    form = MyDjangoForm()

    if request.method == 'POST':
        form = MyDjangoForm(request.POST)
        if form.is_valid():
            print('Validation success')
            print('Name : ' + form.cleaned_data['name'])
            print('Email : ' + form.cleaned_data['email'])
            print('Text: ' + form.cleaned_data['text'])

    return render(request, 'my_django_form.html', {'form': form})


def person(request):
    countries = Country.objects.all
    return render(request, 'person.html', {'countries': countries, 'selected_id': 0})


def register(request):
    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request, 'registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})
