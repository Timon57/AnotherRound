from django.shortcuts import render,get_object_or_404

from .models import Category,Product



def home(request):
    products = Product.products.all()

    context = {
        'products':products,
    }
    return render(request,'ecom/home.html',context)

def product_detail(request,pk):
    product = get_object_or_404(Product,id=pk,in_stock=True)
    context = {
        'product':product
    }
    return render(request,'ecom/product_detail.html',context)

def category_list(request,pk):
    category = get_object_or_404(Category,id=pk)
    products = Product.objects.filter(category=category)
    context = {
        'products' : products,
        'category' : category
    }
    return render(request,'ecom/category.html',context)