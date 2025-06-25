from django.shortcuts import render, get_object_or_404
from .models import ProductModels
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def list_product(request):
    products_list = ProductModels.objects.all()
    product_paginator = Paginator(products_list, 2)  # Show 8 per page
    page = request.GET.get('page', 1)
    page_obj = product_paginator.get_page(page)

    # Manual chunking logic (4 per row)
    def chunk_products(products, size):
        return [products[i:i + size] for i in range(0, len(products), size)]

    chunked_products = chunk_products(list(page_obj), 4)

    context = {
        'products_chunks': chunked_products,
        'page_obj': page_obj
    }
    return render(request, 'products.html', context)

def detail_product(request, product_id):
    product = get_object_or_404(ProductModels, id=product_id)
    return render(request, 'product_details.html', {'product': product})
