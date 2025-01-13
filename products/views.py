from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, ProductItemSerializer, ProductValidateSerializer
from rest_framework import status
from django.db import transaction


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.text = serializer.validated_data.get('text')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.search_words.set(serializer.validated_data.get('search_words'))
        product.save()
        return Response(data=ProductItemSerializer(product).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        # step 1: Collect all products from DB (QuerySet)
        products = (Product.objects.select_related('category')
                    .prefetch_related('search_words', 'reviews').all())

        # step 2: Reformat (Serialize) QuerySet to List of dictionary
        list_ = ProductSerializer(instance=products, many=True).data

        # step 3: Return response as data and status (200)
        return Response(data=list_)
    elif request.method == 'POST':
        # step 0: Validation (Existing, Typing and Extra)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        # step 1: Receive data from ValidatedData
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')  # "Y"
        category_id = serializer.validated_data.get('category_id')
        search_words = serializer.validated_data.get('search_words')

        # step 2: Create product
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                text=text,
                price=price,
                is_active=is_active,
                category_id=category_id,
            )
            product.search_words.set(search_words)
            product.save()

        # step 3: Return response (product, status)
        return Response(data=ProductItemSerializer(product).data, status=status.HTTP_201_CREATED)
