from django.urls import path,include
from .views import *

urlpatterns = [

    path('',home,name='home'),
    # for displaying products
    path('collections',collections,name='category'),
    path('categorydetail/<str:name>',categorydetail,name='categorydetail'),
    path('productview<str:id>',productview,name='product'),
    path("product-list",ajaxlist,name='ajaxlist'),
    path('search',productsearch,name='productsearch'),
    # for the authentications
    path('register',register_user,name='register'),
    path('login',login_user,name='login'),
    path('logout',logout_user,name='logout'),

    # for the cart

    path('add-to-cart',addtocart,name='addtocart'),
    path('yourcart',cart,name='cart'),
    path('updatecart',updatecart,name='updatecart'),
    path('deleteitem',deleteitem,name='deleteitem'),

    # for the wishlist
    path('yourwislist',wishlist,name='wishlist'),
    path('addtowishlist',addtowishlist,name='addwishlist'),
    path('deletewishlistitem',deletewishlistitem,name='deletewishlistitem'),

    path('checkout',checkout,name='checkout'),
    path('place-order',placeorder,name='placeorder'),
    path('your-orders',yourorders,name='yourorders'),
    path('vieworder/<int:pk>',vieworder,name='vieworder'),

    
]