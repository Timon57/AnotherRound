from django.urls import path

from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('item/<slug:pk>',views.product_detail,name='product_detail'),
    path('search/<slug:pk>',views.category_list,name='category_list')
]