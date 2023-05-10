from django.db import models
from django.urls import reverse
# Create your models here.



from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile




def resize_image(image):
    img = Image.open(image)
    output_size = (200, 600)  # Set the desired size for the image
    img.thumbnail(output_size)
    output_io = BytesIO()
    img.save(output_io, format='JPEG', quality=85)
    output_io.seek(0)
    resized_image = InMemoryUploadedFile(output_io, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output_io.getvalue(), None)
    return resized_image


class Category(models.Model):

    name = models.CharField(max_length=200)

    image = models.ImageField(upload_to='category_image//%Y/%m/%d',
                              blank=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_image(self.image)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kobosh:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
                              
    description = models.TextField(blank=True, max_length=200)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_image(self.image)
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('kobosh:product_detail',
            args=[self.id, self.slug])


