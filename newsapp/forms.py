from django.forms import *
from .models import Article,MoreContent

class ArticleForm(ModelForm):
    class Meta:
        model=Article
        fields=['title','short_description','paragraph','category','image','slug']
        widgets={
            'title':TextInput(attrs={"placeholder":"Article Title","class":"form-input"}),
            'short_description':TextInput(attrs={"placeholder":"Article short_description","class":"form-input"}),
            'paragraph':Textarea(attrs={"placeholder":"Article Title","rows":5,"class":"form-input"}),
            'category':Select(attrs={"placeholder":"Article Category","class":"form-input"}),
            'slug':TextInput(attrs={"placeholder":"Article Slug","class":"form-input"})  
    }

class MoreContentForm(ModelForm):
    class Meta:
         model=MoreContent
         fields=['image','short_description','paragraph']
         widgets={
            'short_description':TextInput(attrs={"placeholder":"Short Description","class":"form-input"}),
            'paragraph':Textarea(attrs={"placeholder":" paragraph","rows":5,"class":"form-input"}),
    }

class ArticleUpdateForm(ModelForm):
    class Meta:
        model=Article
        fields=['title','short_description','paragraph','image','slug']
        widgets={
           'title':TextInput(attrs={"placeholder":"Article Title","class":"form-input"}),
            'short_description':TextInput(attrs={"placeholder":"Article short_description","class":"form-input"}),
            'paragraph':Textarea(attrs={"placeholder":"Article Title","rows":5,"class":"form-input"}),
            'category':Select(attrs={"placeholder":"Article Category","class":"form-input"}),
            'slug':TextInput(attrs={"placeholder":"Article Slug","class":"form-input"})  
    }