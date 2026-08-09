from django.shortcuts import render , get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse
from kavenegar import *
from .common.kavenegar_utils import send_sms , send_lookup
# Create your views here.

@require_POST
def add_to_cart(request , product_id):
    try :
        cart = Cart(request)
        product = get_object_or_404(Product , id=product_id)
        cart.add(product)
        context = {
            'item_count':len(cart),
            'total_price':cart.get_total_price(),
        }
        #--------------------------------------------   
        # try:
        #     api = KavenegarAPI('382B63416131706353324446375962696F4D377A3548786D533653516C4456346948744B6A737972414D383D')
        #     params = {
        #         'sender': '2000660110',#optional
        #         'receptor': '09353181207',#multiple mobile number, split by comma
        #         'message': f'{str(product)} add to carrt . GOOD LUCK',
        #     } 
        #     response = api.sms_send(params)
        #     print(response)
        # except APIException as e: 
        #     print(e)
        # except HTTPException as e: 
        #     print(e)
        #--------------------------------------------    
        # try:
        #     api = KavenegarAPI('382B63416131706353324446375962696F4D377A3548786D533653516C4456346948744B6A737972414D383D')
        #     params = {
        #         'receptor': '09353181207',
        #         'template': 'sabz-shop',
        #         'token': 'اشکان',
        #         'token2': '33621',
        #         # 'token3': '',
        #         'type': 'sms',#sms vs call
        #     }   
        #     response = api.verify_lookup(params)
        #     print(response)
        # except APIException as e: 
        #     print(e)
        # except HTTPException as e: 
        #     print(e)
        #--------------------------------------------    
        # send_sms('09353181207' , 'Hi , this product added the cart .')
        # send_lookup('09353181207' , 'sabz-shop' , {'token':'اشکان' , 'token2':'33621'})
        #--------------------------------------------  
        return JsonResponse(context)
    except Exception as e:
        print("REAL ERROR:", e)
        return JsonResponse({'error': 'Invalid request .'})
    

def cart_detail(request):
    cart = Cart(request)
    return render(request , 'cart/detail.html' , {'cart':cart})

@require_POST
def update_quantity(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    try:
        product = get_object_or_404(Product , id=item_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)
        
        context = {
            'item_count':len(cart),
            'total_price':cart.get_total_price(),
            'quantity':cart.cart[item_id]['quantity'],
            'total':cart.cart[item_id]['quantity'] * cart.cart[item_id]['price'],
            'final_price':cart.get_final_price(),
            'success' : True
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'success':False , 'error':'Item not found!'})


@require_POST
def remove_item(request):
    item_id = request.POST.get('item_id')
    try :
        product = get_object_or_404(Product , id=item_id)
        cart = Cart(request)
        cart.remove(product)

        context = {
            'item_count':len(cart),
            'total_price':cart.get_total_price(),
            'final_price':cart.get_final_price(),
            'success' : True
        }
        return JsonResponse(context)
    except : 
        return JsonResponse({'success':False , 'error':'Item not found!'})

