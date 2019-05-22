from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Sections, Product, Category
from ..serializers import SectionsSerializer, ProductSerializer, CategorySerializer2


@api_view(['GET'])
def cart(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        products = request.user.products_purchased
    except Product.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def sections_list(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        sections = category.section_c.all()
        serializer = SectionsSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SectionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def sections_detail(request, pk, pk2):
    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = SectionsSerializer(sections, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SectionsSerializer(instance=sections, data=request.data)
        if serializer.is_valid():
            serializer.save() # update function in serializer class
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        sections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request, pk, pk2):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        product = sections.product.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sections_id=pk2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk, pk2, pk3):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    try:
        product = Product.objects.get(id=pk3)
    except Product.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save() # update function in serializer class
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def purchase_product(request, pk, pk2, pk3):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    try:
        product = Product.objects.get(id=pk3)
    except Product.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        product.purchased_by = request.user
        product.status = "продано"
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
