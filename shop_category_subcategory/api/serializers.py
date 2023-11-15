from rest_framework import serializers
from product.models import Product, SubCategory, Category, Cart, ProductCart



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            'name',
            'slug',
            'image'
        )


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(
        read_only=True,
        many=True
    )
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'image',
            'sub_category'
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    sub_category = SubCategorySerializer(
        read_only=True
    )
    class Meta:
        model = Product
        fields = (
            'category',
            'sub_category',
            'name',
            'slug',
            'large_image',
            'medium_image',
            'small_image',
            'price'
        )


class ProductInCartSerializer(serializers.ModelSerializer):
    price = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = (
            'name',
            'price'
        )


class ProductCartSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    def get_subtotal(self, obj):
        return obj.product.price * obj.amount

    class Meta:
        model = ProductCart
        fields = (
            'product',
            'amount',
            'subtotal',
        )


class CreateCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Cart
        fields = (
            'user',
        )

class CartSerializer(serializers.ModelSerializer):
    product_cart = ProductCartSerializer(
        many=True,
        read_only=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total = 0
        for product in obj.product_cart.all():
            total += product.product.price * product.amount
        return {'total': total}

    class Meta:
        model = Cart
        fields = (
            'product_cart',
            'total'
        )


class ProductCartCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(
        read_only=True
    )
    cart = CartSerializer(
        read_only=True
    )
    class Meta:
        model = ProductCart
        fields = (
            'product',
            'cart'
        )


class CartDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'product_cart']
