from rest_framework import serializers
from .models import Product, Category, SearchWord, Review
from rest_framework.exceptions import ValidationError


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


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=3)
    text = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=10, max_value=1000000)
    is_active = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()
    search_words = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist!')
        return category_id

    def validate_search_words(self, search_words):  # [1,2,12]
        search_words_db = SearchWord.objects.filter(id__in=search_words)  # [1,2]
        if len(search_words) != len(search_words_db):
            raise ValidationError('SearchWord does not exist!')
        return search_words
