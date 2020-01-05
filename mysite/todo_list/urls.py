from django.urls import path
from . import views
urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('logout/', views.user_logout, name='logout'),
   path('accounts/login/', views.user_login, name='login'),
   path('user_login/', views.user_login, name='user_login'),
   path('search/', views.search, name='search'),
   path('summary/', views.summary, name='summary'),
   path('guest', views.guest, name='guest'),
   path('denied', views.denied, name='denied'),
   path('create/', views.CoinCreateView.as_view(), name='create_coin'),
   path('update/<int:pk>', views.CoinUpdateView.as_view(), name='update_coin'),
   path('read/<int:pk>', views.CoinReadView.as_view(), name='read_coin'),
   path('delete/<int:pk>', views.CoinDeleteView.as_view(), name='delete_coin'),
   path('coins_list/<category>', views.coins_list, name='coins_list'),
   path('coins_list_json', views.CoinsListJson.as_view(), name="coins_list_json"),
   path('coins_search_json', views.CoinsSearchJson.as_view(), name="coins_search_json"),

]
