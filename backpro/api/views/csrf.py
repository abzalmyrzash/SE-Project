import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from ..models import Category, Sections, Product, Basket
from django.views.decorators.csrf import csrf_exempt
from ..serializers import CategorySerializer, CategorySerializer2,SectionsSerializer, ProductSerializer, BasketSerializer


@csrf_exempt
def sections_list(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    if request.method == "GET":
        sections = category.section_c.all()
        serializer = SectionsSerializer(sections, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        data = json.loads(request.body)
        serializer = SectionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(category_id=pk)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def sections_detail(request, pk, pk2):
    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)
    if request.method == "GET":
        serializer = SectionsSerializer(sections, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        data = json.loads(request.body)
        serializer = SectionsSerializer(instance=sections, data=data)
        if serializer.is_valid():
            serializer.save() # update function in serializer class
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        sections.delete()
        return JsonResponse({})


@csrf_exempt
def product_list(request, pk, pk2):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    if request.method == "GET":

        product = sections.product.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        data = json.loads(request.body)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sections_id=pk2)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def product_detail(request, pk, pk2, pk3):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    try:
        product = Product.objects.get(id=pk3)
    except Product.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)
    if request.method == "GET":
        serializer = ProductSerializer(product, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        data = json.loads(request.body)
        serializer = ProductSerializer(instance=product, data=data)
        if serializer.is_valid():
            serializer.save() # update function in serializer class
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        product.delete()
        return JsonResponse({})



@csrf_exempt
def purchase_product(request, pk, pk2, pk3):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    try:
        sections = Sections.objects.get(id=pk2)
    except Sections.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    try:
        product = Product.objects.get(id=pk3)
    except Product.DoesNotExist as e:
        error = {
            'error': str(e)
        }
        return JsonResponse(error, safe=False)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authorized'}, status=401)

        data = json.loads(request.body)
        product.purchased_by = request.user
        product.save()
        serializer = ProductSerializer(instance=product, data=data)
        if serializer.is_valid():
            serializer.save()  # update function in serializer class
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    return JsonResponse({'error': 'bad request'})
