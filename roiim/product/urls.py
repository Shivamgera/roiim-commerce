from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^(?P<product_pk>[0-9]+)/$",
        views.product_details,
        name="details",
    ),
    url(
        r"^$",
        views.product_list,
        name="list",
    )
]