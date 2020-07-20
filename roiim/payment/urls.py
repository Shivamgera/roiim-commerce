from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^(?P<product_pk>[0-9]+)/$",
        views.payment_start,
        name="start",
    ),
    url(
        r"^(?P<product_pk>[0-9]+)/details/$",
        views.payment_details,
        name="details",
    ),
    url(
        r"^(?P<product_pk>[0-9]+)/details/(?P<payment_pk>[0-9]+)/success/$",
        views.payment_success,
        name="success",
    ),
    url(
        r"^(?P<product_pk>[0-9]+)/details/(?P<payment_pk>[0-9]+)/complete/$",
        views.payment_final,
        name="final",
    ),
      url(
        r"^order/details/$",
        views.order_details,
        name="order-details",
    ),
]