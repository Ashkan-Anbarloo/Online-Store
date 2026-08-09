from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import PhoneVerificationForm , OrderCreateForm
from .models import OrderItem , Order
from cart.cart import Cart
from account.models import ShopUser
import random
from django.contrib.auth import login
from cart.common.kavenegar_utils import send_lookup , send_sms
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
import requests
import json
# Create your views here.

def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:order_create')
    if request.method == 'POST':
        if request.method == 'POST':
            form = PhoneVerificationForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                if ShopUser.objects.filter(phone=phone).exists():
                    messages.error(request , 'this phone is already registered . ')
                    return redirect('orders:verify_phone')
                else:
                    tokens = {'token': ''.join(random.choices('0123456789' , k=6))}
                    request.session['verification_code'] = tokens['token']
                    request.session['phone'] = phone
                    print(tokens)
                    # send_lookup('09353181207' , 'sabz_shop' , {'token':'ashkan' , 'token2':tokens})
                    messages.error(request , 'verification code sent successfully . ')
                    return redirect('orders:verify_code')
    else:
        form = PhoneVerificationForm()
    return render(request , 'orders/verify_phone.html' , {'form':form})



def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code :
                user = ShopUser.objects.create_user(phone=phone)
                user.set_password('123456')
                user.save()
                # send sms
                print(user)
                login(request , user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('orders:order_create')
            else:
                messages.error(request , 'Verification code is incorrect.')
    return render(request , 'orders/verify_code.html')



@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'],weight=item['weight'])
            # cart.clear()
            return redirect('orders:request')
                                                    
    else:
        form = OrderCreateForm()
    
    context = {
        'form':form,
        'cart':cart,
    }
    return render(request , 'orders/order_create.html' , context)

#--------------------

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/order/verify/'


def send_request(request):
    # order = Order.objects.get(id=request.session['order_id'])
    cart = Cart(request)
    description = ""
    for item in cart:
        description += item['product'].name + ", "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": cart.get_final_price(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                cart.clear()
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(authority):
    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response