from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # path('' , views.home , name='home'),
    #products/
    path('' , views.product_list , name='product_list'),
    path('products/<slug:category_slug>/' , views.product_list , name='product_list_by_category'),
    path('product/<int:id>/comment/', views.post_comment, name='product_comment'),
    path('product/<int:id>/<slug:slug>/' , views.product_detail , name='product_detail'),
    path('like_post/' , views.like_post , name='like_post'),
]
