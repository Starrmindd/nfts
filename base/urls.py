from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('listnft',views.listnft,name="listnft"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('nfts/<int:nft_id>/', views.nft_detail, name='nft_detail'),
    path('nfts/list/', views.nft_list, name='nft_list'),
]

