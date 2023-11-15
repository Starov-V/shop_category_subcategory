from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from product.models import Product, Category, Cart, ProductCart
from . import serializers, permissions


class ProductViewSet(
      viewsets.GenericViewSet,
      mixins.ListModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = (AllowAny, )


class CategoryViewSet(
      viewsets.GenericViewSet,
      mixins.ListModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AllowAny, )


class ShowDeleteCartView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        user = request.user
        cart = Cart.objects.filter(user=user).get()
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    
    def delete(self, request):
        user = request.user
        cart = user.cart
        for product in cart.product_cart.all():
            product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class AddChangeDeleteProductView(APIView):
    serializer_class = serializers.ProductCartCreateSerializer
    permission_classes = (permissions.IsOwner, )

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(
            id=self.kwargs.get('product_id')).get()
        user = self.request.user
        cart = Cart.objects.filter(user=user).get()
        if ProductCart.objects.filter(
            product=product,
            cart=cart
        ).exists():
            product_cart = ProductCart.objects.filter(
                product=product,
                cart=cart
            )
            product = product_cart.get()
            product.amount += 1
            product.save()
            serializer = serializers.ProductCartCreateSerializer(product)
            return Response(serializer.data)
        data = {
            'product': product,
            'cart': cart,
            'amount': 1
        }
        serializer = serializers.ProductCartCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                product=product,
                cart=cart,
                amount=1)
            return Response(serializer.data)
        
    def delete(self, request, *args, **kwargs):
        product = Product.objects.filter(
            id=self.kwargs.get('product_id')).get()
        user = self.request.user
        cart = Cart.objects.filter(user=user).get()
        if ProductCart.objects.filter(
            product=product,
            cart=cart
        ).exists():
            product_cart = ProductCart.objects.filter(
                product=product,
                cart=cart
            )
            product = product_cart.get()
            if product.amount > 1:
                product.amount -= 1
            else:
                product.delete()
                serializer = serializers.ProductCartCreateSerializer(product)
                return Response(serializer.data)
            product.save()
            serializer = serializers.ProductCartCreateSerializer(product)
            return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        product = Product.objects.filter(
            id=self.kwargs.get('product_id')).get()
        user = self.request.user
        cart = Cart.objects.filter(user=user).get()
        product_cart = ProductCart.objects.filter(
            product=product,
            cart=cart
        ).get()

        data=request.data

        product_cart.amount = data.get("amount", product_cart.amount)

        product_cart.save()
        serializer = serializers.ProductCartCreateSerializer(product_cart)

        return Response(serializer.data)
