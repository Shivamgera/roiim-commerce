from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"^signup/(?P<product_pk>[0-9]+)/$",
        views.signup,
        name="signup",
    ),
    url(
        r"^logout/$",
        views.logout,
        name="logout",
    ),
    url(
        r"^login/$",
        views.login,
        name="login",
    ),
]