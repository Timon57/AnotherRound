from django.shortcuts import render
from .cart import Cart
from ecom.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    context = {'cart':cart}
    return render(request,'cart/summary.html',context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product,id=product_id)
        cart.add( product_qty,product=product)
        cartqty = cart.__len__()
        response = JsonResponse({'qty':cartqty})
        return response
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product=product_id)
        carttotal = cart.get_total_price()
        cartqty = cart.__len__()
        response = JsonResponse({'qty':cartqty,'total':carttotal})
        return response
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        cart.update(product=product_id,qty=product_qty)
        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        print(cartqty)
        print(carttotal)
        response = JsonResponse({'qty':cartqty,'total':carttotal})
        return response

    
