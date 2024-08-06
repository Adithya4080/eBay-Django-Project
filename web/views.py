import json
import random
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.http import JsonResponse
from web.models import Product,SavedItem, Category,Gallery,Specification
from django.forms import modelformset_factory



def index(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')  
    
    products = []
    recent = []
    picks = []
    watches = []

    
    if query:
        products = Product.objects.filter(name__icontains=query)
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()       
    else:
        recent = Product.objects.all()[:6]
        picks = Product.objects.all()[6:12]
        watches = Product.objects.all()[12:18]
    
    
    context = {
        "products": products,
        "recents": recent,
        "picks": picks,
        "watches": watches,
        "query": query,
        "category_slug": category_slug,
    }

    return render(request, "index.html", context=context)


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = product.category.all()
    similar_products = Product.objects.filter(category__in=categories).exclude(id=product_id).distinct()[:6]
    gallery_images = Gallery.objects.filter(name=product)
    available_stock = random.randint(1, product.stock - 1)
    specifications = Specification.objects.filter(product=product)


    context = {
        "product":product,
        "categories":categories,
        'similar_products': similar_products,
        'gallery_images': gallery_images,
        'available_stock': available_stock,
        'specifications': specifications,
    }
    return render(request, 'productDetails.html',context=context)


def save_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    saved_item, created = SavedItem.objects.get_or_create(product=product)


    if not created:
        saved_item.delete()
        saved = False
    else:
        saved = True

    return JsonResponse({'saved': saved})


def saved_items(request):
    saved_items = SavedItem.objects.all()
    print(f"Number of saved items: {saved_items.count()}")
    context = {
        'saved_items': saved_items
    }
    return render(request, 'savedItems.html', context)


def fetch_items(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        items = category.products.all()
        items_data = [
            {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'image_url': item.image.url if item.image else '',
            }
            for item in items
        ]
        return JsonResponse({'items': items_data})
    except Category.DoesNotExist:
        return JsonResponse({'items': []})
    

def category_items(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = category.products.all()
    
    items_data = [{
        'id': item.id,
        'name': item.name,
        'price': str(item.price),
        'image_url': item.image.url if item.image else '',
    } for item in items]
    
    data = {
        'category_name': category.name,
        'items': items_data,
    }
    
    return JsonResponse(data)