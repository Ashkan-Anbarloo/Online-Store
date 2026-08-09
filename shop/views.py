from django.shortcuts import render , get_object_or_404 , redirect
from .models import Category , Product
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
# Create your views here.

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('account:login')
    user = request.user
    return render(request , 'shop/home.html' , {})


def product_list(request , category_slug=None):
    categorise = Category.objects.all()

    if category_slug :
        category = get_object_or_404(Category , slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        category = None
        products = Product.objects.all()
    
    sort_by = request.GET.get('sort', 'newest') 
    if sort_by == 'cheapest':
        products = products.order_by('new_price') 
    else:
        products = products.order_by('-created')

    paginator = Paginator(products , 4)
    page_number = request.GET.get('page' , 1)
    try:
        products = paginator.page(page_number)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)
        
    context = {
        'category':category,
        'categories':categorise,
        'products':products,
        'sort_by': sort_by,
    }

    return render(request , 'shop/list.html' , context)



def product_detail(request , id , slug):
    product = get_object_or_404(Product , slug=slug , id=id)
    related_products = (
        Product.objects.filter(category=product.category).exclude(id=product.id).order_by('-created')[:4]
    )
    context = {
        'product':product,
        'related_products':related_products,
    }
    return render(request , 'shop/detail.html' , context)
