from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('all_product/', views.all_product, name='all_product'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),

    path('<slug:category_slug>/', views.home, 
        name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
        name = 'product_detail'),
]