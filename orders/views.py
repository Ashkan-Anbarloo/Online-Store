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
            # order = form.save()
            # order.buyer = request.user
            # order.save()
            # for item in cart:
            #     OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'],weight=item['weight'])
            # cart.clear()
            request.session['order_data'] = form.cleaned_data
            return redirect('orders:order_confirm')
                                                    
    else:
        form = OrderCreateForm()
    
    context = {
        'form':form,
        'cart':cart,
    }
    return render(request , 'orders/order_create.html' , context)

#--------------------
# orders/views.py

def order_confirm(request):
    cart = Cart(request)
    order_data = request.session.get('order_data')

    # اگر کاربر مستقیم به این آدرس بیاید و اطلاعاتی در سشن نباشد
    if not order_data:
        return redirect('orders:order_create')

    if request.method == 'POST':
        # مرحله نهایی: ایجاد سفارش و پرداخت
        order = Order.objects.create(
            buyer=request.user,
            paid=True, # تنظیم وضعیت پرداخت به True
            **order_data
        )
        
        # ذخیره آیتم‌ها
        for item in cart:
            OrderItem.objects.create(
                order=order, 
                product=item['product'], 
                price=item['price'], 
                quantity=item['quantity'], 
                weight=item['weight']
            )
        
        # پاکسازی
        cart.clear() # خالی کردن سبد
        del request.session['order_data'] # حذف اطلاعات از سشن
        
        return redirect('shop:product_list')

    return render(request, 'orders/order_confirm.html', {
        'order_data': order_data, 
        'cart': cart
    })

