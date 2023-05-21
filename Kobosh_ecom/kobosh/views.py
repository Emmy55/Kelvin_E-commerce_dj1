
from . models import Category, Product 
from django.shortcuts import render

from cart.forms import CartAddProductForm

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required


import re
from bs4 import BeautifulSoup
from django.db.models import Q


def home(request,category_slug=None):
    category = None
    categories = Category.objects.all()

    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    
    context={'category' : category,
        'categories': categories,
        'products': products}
    if request.resolver_match.url_name == 'home':
        template_name = 'kobosh/home.html'
    else:
        template_name = 'kobosh/categories.html'
    return render(request, template_name, context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()
    return render(request,
                  'kobosh/details.html',
                  {'product' : product,
                    'cart_product_form': cart_product_form})


def payment(request):
    return render(request, 'kobosh/payments.html')




def search(request):
    query = request.GET.get('query')
    results = []

    if query:
        # Search the database for products matching the query
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        # Iterate over the retrieved products
        for product in products:
            name = product.name
            image = product.image.url
            price = product.price

            # Append the product information to the results list
            results.append({'name': name, 'image': image, 'price': price})
            print(results)

    return render(request, 'kobosh/result.html', {'results': results})

