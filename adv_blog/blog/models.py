from django.db import models
from django.utils import timezone 
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.
USER = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(USER, on_delete=models.CASCADE) 
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(upload_to = 'images/', default = 'images/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=timezone.now) 
    slug = models.SlugField(blank=True)

    def save(self):
        self.slug = slugify(self.title)
        return super(Post, self).save()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug':self.slug})
