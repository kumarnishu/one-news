from django.contrib import admin
from .models import Article,Category,MoreContent

# Register your models here.
class MoreContentInline(admin.StackedInline):
    model=MoreContent
    extra=0
class ArticleAdmin(admin.ModelAdmin):
    inlines=[
    MoreContentInline,
    ]
    list_display=('category','author','title','published')
    verbose_name="Category"
    verbose_name_plural="Categories"

admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(MoreContent)