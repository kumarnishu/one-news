from django.db import models
from django.conf import settings
from django.urls import reverse

# article category model
class Category(models.Model):
        category=models.CharField(max_length=200)
        slug=models.SlugField(unique=True,max_length=400)
        class Meta:
            verbose_name = "category"
            verbose_name_plural = "categories"
        def __str__(self):
            return self.category 

# article model
class Article(models.Model):
    title=models.CharField(max_length=200)
    short_description=models.CharField(max_length=400)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    paragraph=models.TextField(max_length=2000)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="article/images")
    slug=models.SlugField("Permalink",unique=True,max_length=400)
    last_updated=models.DateTimeField(auto_now=True)
    published=models.BooleanField(default=False)
    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ["-last_updated"]
    def __str__(self):
        return  self.title
    def get_absolute_url(self):
        return reverse('newsapp:NewsDetail', kwargs={'slug': self.slug})

# more content to the article
class MoreContent(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="article/images",null=True,blank=True)
    short_description=models.CharField(max_length=200)
    paragraph=models.TextField(max_length=2000)
    class Meta:
        verbose_name = "more cotent for articles"
        verbose_name_plural = "more cotent for articles"
    def __str__(self):
        return self.short_description

