"""
URL configuration for ardueshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("auth/", include(("authentication.urls", "authentication"), namespace="authentication")),
        path("product/", include("product.urls", namespace="product")),
        path("catalogue/", include("product.urls", namespace="catalogue")),
        path("cart/", include("cart.urls", namespace="cart")),
        path("order/", include("order.urls", namespace="order")),
        path("payment/", include("payment.urls", namespace="payment")),
        path(
            "", include("base.urls")
        ),  # This path must be the last one because it will match any URL
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
