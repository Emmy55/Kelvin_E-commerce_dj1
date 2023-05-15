from django.shortcuts import render, redirect, get_object_or_404
from kobosh.models import Product
from .cart import Cart
from .forms import CartAddProductForm

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')   

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'kobosh/cart.html', {'cart': cart})


# views.py
import re

def search(request):
    query = request.GET.get('query')
    results = []

    from bs4 import BeautifulSoup

    if query:
        # Specify the HTML file to search
        html_file_path = 'kobosh/templates/kobosh/categories.html'
    
        # Read the content of the HTML file
        with open(html_file_path, 'r') as file:
            page_content = file.read()
    
        # Parse the HTML content
        soup = BeautifulSoup(page_content, 'html.parser')
    
        # Find relevant elements in the parsed HTML
        results = []
        for element in soup.find_all('div', class_='product'):
            name = element.find('h3').text
            description = element.find('p', class_='description').text
            image = element.find('img')['src']
            price = element.find('p', class_='price').text
    
            # Check if the query matches any information
            if query.lower() in (name.lower() + description.lower()):
                results.append({'name': name, 'description': description, 'image': image, 'price': price})
    
    return render(request, 'kobosh/results.html', {'query': query, 'results': results})
