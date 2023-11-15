from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)

urlpatterns = [
    re_path(r'products/(?P<product_id>\d+)/',
            views.AddChangeDeleteProductView.as_view()),
    path('cart/', views.ShowDeleteCartView.as_view()),
    path('', include(router.urls)),
]
