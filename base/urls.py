from django.urls import path
from . import views

urlpatterns = [
   
    # path('list/<int:token_id>/', views.list_nft_for_sale, name='list_nft_for_sale'),
    # path('buy/<str:token_id>/', views.buy_nft, name='buy_nft'),
    # # path('listnft',views.listnft,name="listnft"),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    # path('nfts/<int:nft_id>/', views.nft_detail, name='nft_detail'),
    # path('nfts/list/', views.nft_list, name='nft_list'),
     path('delist_nft/<int:pk>/', views.delist_admin, name='delist_nft'),
    path('list_admin/<int:pk>/', views.list_admin, name='list_admin'),
    path('list_sale', views.list_nft_for_sale, name='list_sale'),
    path('adminview', views.adminview, name='adminview'),
    path('delist_admin', views.delist_admin, name='delist_admin'),
    path('purchase', views.buyer_nft_list, name='purchase'),
    path('create/', views.create_auction, name='create_auction'),
    path('list/', views.auction_list, name='auction_list'),
    path('detail/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('buy_nft/<str:nft_title>/', views.buy_nft, name='buy_nft'),
]

