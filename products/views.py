from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ProductSerializer(product).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    # step 1: Collect all products from DB (QuerySet)
    products = Product.objects.all()

    # step 2: Reformat (Serialize) QuerySet to List of dictionary
    list_ = ProductSerializer(instance=products, many=True).data

    # step 3: Return response as data and status (200)
    return Response(data=list_)
