from django.urls import path
from .views import SampleView, ProductOne, ProductTwo

urlpatterns = [
    path("sample/", SampleView.as_view(), name="sample"),
    path("product/one/", ProductOne.as_view(), name="product_one"),
    path("product/two/", ProductTwo.as_view(), name="product_two"),
]
