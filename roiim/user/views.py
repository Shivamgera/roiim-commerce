from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from ..product.models import Product
from .forms import SignupForm, LoginForm

# Create your views here.

def signup(request, product_pk):
    print(request.user)
    if request.user.is_authenticated:
        return redirect(reverse('product:details', kwargs={'product_pk':product_pk}))
    product = Product.objects.get(pk=product_pk)
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        user = auth.authenticate(request=request, username=username, password=password)
        try:
            if user:
                auth.login(request, user)
        except Exception as e:
            print(e)
        messages.success(request, ("User has been created"))
        # redirect_url = request.POST.get("next", "http://localhost:8000/products/1")
        redirect_url = reverse('product:details', kwargs={'product_pk':product_pk})
        return redirect(redirect_url)
    ctx = {
            "form": form,
            "product":product, }
    return TemplateResponse(request, "user/signup.html", ctx)

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, ("You have been successfully logged out."))
    return redirect(reverse('product:list'))

def login(request):
    kwargs = {"template_name": "user/login.html", "authentication_form": LoginForm}
    return django_views.LoginView.as_view(**kwargs)(request, **kwargs)