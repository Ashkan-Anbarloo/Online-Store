from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255 , unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
    

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])
    

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category , related_name='products' , on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=1200)
    inventory = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    # features = models.ForeignKey(ProductFeature , related_name=)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id' , 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id ,self.slug])
    
    def __str__(self):
        return self.name
    


class ProductFeature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product , related_name='features' , on_delete=models.CASCADE)
    def __str__(self):
        return self.name + ':' + self.value



class Image(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='images')
    # image_file = models.ImageField(upload_to='post_images/')
    file = models.ImageField(upload_to="product_images/%Y/%m/%d")
    description = models.TextField(null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)    

    class Meta:
        ordering = ['-created',]
        indexes = [
            models.Index(fields=['-created']),
        ]


class Comment(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created',]
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.product.description[:10]}"