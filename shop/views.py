from django.shortcuts import render , get_object_or_404 , redirect
from .models import Category , Product
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.

# def home(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('account:login')
#     user = request.user
#     return render(request , 'shop/home.html' , {})


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


@login_required
def product_detail(request , id , slug):
    product = get_object_or_404(Product , slug=slug , id=id)
    related_products = (
        Product.objects.filter(category=product.category).exclude(id=product.id).order_by('-created')[:4]
    )
    comments = product.comments.all()
    form = CommentForm()
    context = {
        'product':product,
        'related_products':related_products,
        'comments':comments,
        'form':form,
    }
    return render(request , 'shop/detail.html' , context)


@login_required
def post_comment(request , id):
    product = get_object_or_404(Product , id=id)
    comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            # comment.name = (
            #     getattr(request.user, 'get_full_name', lambda: '')().strip()
            #     or getattr(request.user, 'username', '')
            #     or str(request.user)
            # )
            comment.name = request.user.first_name
            comment.save()
            return JsonResponse({
                'status': 'ok',
                'name': comment.name,
                'body': comment.body,
                'created': comment.created,
            })
    else : 
        form = CommentForm()
        
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    # context = {
    #     'product' : product,
    #     'form' : form,
    #     'comment' : comment,
    # }
    # return render(request , 'forms/comment.html' , context)
    # return render(request , 'shop/detail.html' , context)


@login_required
@require_POST
def like_post(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        product = get_object_or_404(Product , id=product_id)
        user = request.user

        if user in product.likes.all():
            product.likes.remove(user)
            liked = False
        else:
            product.likes.add(user)
            liked = True
        product_likes_count = product.likes.count()
        response_data = {
            'liked':liked,
            'liked_count':product_likes_count,
        }
    else:
        response_data = {'error':'Invalid post_id'}
    return JsonResponse(response_data)
