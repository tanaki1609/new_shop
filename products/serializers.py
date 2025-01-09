from rest_framework import serializers
from .models import Product, Category, SearchWord, Review


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']


class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWord
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    search_words = SearchWordSerializer(many=True)
    category_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = 'id title category category_name search_words search_word_list reviews'.split()
        # depth = 1
        # exclude = 'id price'.split()

    def get_category_name(self, product):
        try:
            return product.category.name
        except:
            return 'no category'
