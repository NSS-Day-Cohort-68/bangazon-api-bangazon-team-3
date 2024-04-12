from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapi.models import *
from bangazonapi.views import *
from bangazonapi.views import expensive_products_report
from bangazonapi.views import inexpensive_products_report
from bangazonapi.views import orders_report

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r"products", Products, "product")
router.register(r"productcategories", ProductCategories, "productcategory")
router.register(r"lineitems", LineItems, "orderproduct")
router.register(r"customers", Customers, "customer")
router.register(r"users", Users, "user")
router.register(r"orders", Orders, "order")
router.register(r"cart", Cart, "cart")
router.register(r"paymenttypes", Payments, "payment")
router.register(r"profile", Profile, "profile")
router.register(r"stores", Stores, "store")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "reports/expensiveproducts",
        expensive_products_report,
        name="expensive_products_report",
    ),
    path(
        "reports/inexpensiveproducts",
        inexpensive_products_report,
        name="inexpensive_products_report",
    ),
    path(
        "reports/favoritesellers",
        favorite_sellers_by_customer_report,
        name="favorite_sellers_by_customer_report",
    ),
    path('reports/orders', orders_report, name='orders_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
