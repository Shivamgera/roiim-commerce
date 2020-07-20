"""roiim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from .product.urls import urlpatterns as product_urls
from .user.urls import urlpatterns as user_urls
from .payment.urls import urlpatterns as payment_urls
from .product.views import base, login_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^products/", include((product_urls, "product"), namespace="product")),
    path('', base),
    url(r"^user/", include((user_urls, "user"), namespace="user")),
    url(r"^payment/", include((payment_urls, "payment"), namespace="payment")),
    url(r"^accounts/profile/", login_redirect),
]
