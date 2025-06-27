from django.shortcuts import render, get_object_or_404
from .models import ProductModels
from django.core.paginator import Paginator

def index(request):
    featured_product = ProductModels.objects.order_by('priority')[:4]
    latest_product = ProductModels.objects.order_by('-id')[:4]
    context = {
        'featured_products': featured_product,
        'latest_products': latest_product
    }
    return render(request, 'index.html', context)

def list_product(request):
    products_list = ProductModels.objects.order_by('-priority')
    product_paginator = Paginator(products_list, 2)  # 2 products per page
    page = request.GET.get('page', 1)
    page_obj = product_paginator.get_page(page)

    def chunk_products(products, size):
        return [products[i:i + size] for i in range(0, len(products), size)]

    chunked_products = chunk_products(list(page_obj), 4)

    context = {
        'products_chunks': chunked_products,
        'page_obj': page_obj
    }
    return render(request, 'products.html', context)

def detail_product(request, pk):
    product = get_object_or_404(ProductModels, pk=pk)
    context = {'product': product}
    print(product.url)
    return render(request, 'product_details.html', context)
