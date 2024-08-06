from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    class Meta:
        db_table = "web_category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/images/',blank=True)
    featured_image = models.ImageField(upload_to='products/images/',blank=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    stock = models.IntegerField()

    class Meta:
        db_table = "web_product"

    def __str__(self):
        return self.name
    

class SavedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    saved = models.BooleanField(default=False)
    class Meta:
        db_table = "web_saved"

    def __str__(self):
        return str(self.product)
    

class Gallery(models.Model):
    image = models.ImageField(upload_to='products/images')
    name = models.ForeignKey("web.Product",on_delete=models.CASCADE)

    class Meta:
        db_table = "web_gallery"
        verbose_name_plural = "gallery"

    def __str__(self):
        return str(self.id)
    

class Specification(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "web_specification"
        verbose_name_plural = "specifications"

    def __str__(self):
        return f"{self.key}: {self.value}"