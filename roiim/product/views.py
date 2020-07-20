from django.shortcuts import render, redirect, reverse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from .models import Product


def base(request):
    return redirect(reverse("product:list"))

def login_redirect(request):
    return redirect(reverse("product:list"))    

def product_list(request):
    products = Product.get_all_products()
    ctx = {"products": products}
    return TemplateResponse(request, 'product/product_list.html', ctx)

@login_required
def product_details(request, product_pk):
    if not request.user.is_authenticated:
        return redirect(reverse('product:list'))
    product = Product.objects.get(pk=product_pk)
    user = request.user
    ctx={
            "product": product,
            "user": user,
        }
    return TemplateResponse(request, 'product/product_details.html', ctx)