
from . models import Category, Product 
from django.shortcuts import render

from cart.forms import CartAddProductForm

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required



def home(request, category_slug=None):
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






def cart(request):
    return render(request, 'kobosh/cart.html')


@login_required(login_url='login')

def signup(request):
    if request.method == 'POST':
        fname=request.POST.get("fname")
        sname=request.POST.get("sname")
        email=request.POST.get("email")
        pass1=request.POST.get("pass")
        pass2=request.POST.get("cpass")
        uname = str(fname) + ' ' + str(sname)
        if pass1 != pass2:
            return HttpResponse("Password varies")

        else:

            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('home')
        
    return render(request, 'kobosh/signup.html')




def login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect.")

    return render(request, 'kobosh/login.html')

def forgotpassword(request):
    return render(request, 'kobosh/forgotpass.html')
