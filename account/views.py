from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponse , JsonResponse
from .forms import UserRegisterForm , AddressForm , UserEditForm
from django.contrib.auth.decorators import login_required
from .models import Address
# Create your views here.

def log_out(request):
    logout(request)
    return render(request , 'registration/logged_out.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            return redirect('shop:home')
    else:
        user_form = UserRegisterForm()
        address_form = AddressForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'address_form': address_form,
    })



@login_required
def edit_user(request):
    user = request.user
    address = Address.objects.filter(user=user).first()

    user_form = UserEditForm(request.POST or None, instance=user)
    address_form = AddressForm(request.POST or None, instance=address)

    if request.method == 'POST':
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            addr = address_form.save(commit=False)
            addr.user = user
            addr.save()
            return redirect('shop:home')

    return render(request, 'registration/edit_user.html', {
        'user_form': user_form,
        'address_form': address_form,
    })