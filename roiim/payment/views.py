from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages

from ..product.models import Product
from .models import CardDetails, Payment

@login_required
def payment_start(request, product_pk):
    if not request.user.is_authenticated:
        return redirect(reverse("product:list"))
    product = Product.objects.get(pk=product_pk)
    user = request.user
    ctx = {
        "product": product,
        "user":user,
    }
    return TemplateResponse(request, "payment/start.html", ctx)


@login_required
def payment_details(request, product_pk):
    if not request.user.is_authenticated:
        return redirect(reverse("product:list"))
    product = Product.objects.get(pk=product_pk)
    user = request.user
    card_number = request.POST.get('cardnumber')
    expiry_month = request.POST.get('expirymonth')
    expiry_year = request.POST.get('expiryyear')
    holder_name = request.POST.get('holdername')
    cv_code = request.POST.get('cvcode')
    remember = request.POST.get('remember')
    amount = product.price
    # if remember:
    CardDetails.save_card(card_number, expiry_month, expiry_year, holder_name, user)
    nickname = request.POST.get('nickname')
    street = request.POST.get('street')
    city = request.POST.get('city')
    postal_code = request.POST.get('zip')
    country = request.POST.get('country')
    response = Payment.create_payment_handle(
        card_number, expiry_month, expiry_year,
        holder_name, cv_code, amount, nickname,
        street, city, postal_code, country, product
    )
    r = response.json()
    if response.status_code == 201:
        return redirect(reverse('payment:success', kwargs={'product_pk':product_pk, 'payment_pk':r['merchantRefNum']}))
    
    messages.error(request, ("Error: something went wrong"))
    ctx = {
        "product": product,
        "user":user,
    }
    return TemplateResponse(request, "payment/start.html", ctx)

@login_required
def payment_success(request, product_pk, payment_pk):
    product = Product.objects.get(pk=product_pk)
    payment = Payment.objects.get(pk=payment_pk)
    user = request.user
    # if not payment.status == Payment.STATUS_SUCCESS:
    #     Payment.pay_for_product(product, payment)

    ctx = {
        "product": product,
        "user":user,
        "payment":payment,
    }
    return TemplateResponse(request, "payment/detail.html", ctx)

@login_required
def payment_final(request, product_pk, payment_pk):
    product = Product.objects.get(pk=product_pk)
    payment = Payment.objects.get(pk=payment_pk)
    user = request.user
    if not payment.status == Payment.STATUS_SUCCESS:
        response = Payment.pay_for_product(product, payment)
    else:
        messages.success(request, ("You already did the payment!"))
        return redirect(reverse("payment:order-details"))
    if response.status_code == 201:
        return redirect(reverse("payment:order-details"))
    messages.error(request, ("Error: something went wrong"))
    ctx = {
        "product": product,
        "user":user,
        "payment":payment,
    }
    return TemplateResponse(request, "payment/detail.html", ctx)

@login_required
def order_details(request):
    user = request.user
    # products = Product.objects.filter(payment__card__user=user)
    cards = CardDetails.objects.filter(user=user)
    payments = Payment.objects.filter(card__in=cards, status=Payment.STATUS_SUCCESS)
    products = Product.objects.filter(payment__in=payments)

    ctx = {
        "products": products,
        "user": user,
    }
    return TemplateResponse(request, "payment/orders.html", ctx)


