from django.urls import path
from . import views

app_name = "kobosh"

urlpatterns = [
    path('', views.home, name='home'),
    path('cate/', views.home, name='cate'),
    path('<slug:category_slug>/', views.home, 
        name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
        name = 'product_detail'),
]