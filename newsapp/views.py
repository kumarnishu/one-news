from django.urls import reverse_lazy
from django.shortcuts import redirect,render
from django.views.generic import ListView,DetailView,TemplateView,CreateView,UpdateView,DeleteView,FormView
from .models import Article,Category,MoreContent
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleForm,ArticleUpdateForm,MoreContentForm
from django.forms import modelformset_factory
from django.http import Http404,HttpResponse
from django.contrib import messages

# staff mixin
class CheckStaffMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff :
            return super().dispatch(request, *args, **kwargs)
        messages.info(self.request,"Sorry ! must me a staff or admin")
        return redirect("newsapp:Index")

#home page view
class Index(ListView):
    model=Article
    context_object_name='articles'
    template_name="newsapp/index.html"
    paginate_by=10  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()[:5]
        return context

#news detail view
class NewsDetail(DetailView):
    model=Article
    context_object_name="article"
    template_name="newsapp/article_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = Article.objects.filter(category__category__contains=self.object.category).exclude(slug=self.object.slug)[:3]
        context['categories']=Category.objects.all()[:5]
        context['more_news']=Article.objects.all().exclude(category=self.object.category)[:8]
        context['more_detail']=MoreContent.objects.filter(article=self.object)
        return context
# news by category
class NewsByCategory(ListView):
    model=Category
    template_name="newsapp/index.html"
    paginate_by=10
    context_object_name="articles"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()[:5]
        return context
    def get_queryset(self, *args, **kwargs):
        category=Category.objects.get(slug=self.kwargs['slug'])
        return Article.objects.filter(category__category__contains=category.category)

#search view
class Search(ListView):
    model=Article
    template_name="newsapp/index.html"
    context_object_name="articles"
    paginate_by=10  
    def get_queryset(self):
        query = self.request.GET.get("search")
        return Article.objects.filter(Q(title__icontains=query)|Q(short_description__icontains=query) | Q(paragraph__icontains=query))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()[:5]
        return context

#create news view
class CreateArticle(CheckStaffMixin,CreateView):
    model=Article
    form_class=ArticleForm
    template_name="newsapp/create_article.html"
    def form_valid(self, form):
       article=form.save(commit=False)
       article.author=self.request.user
       article.save()
       messages.info(self.request,"new article added")
       return redirect("newsapp:MoreContentAdd",article.slug)

class MoreContentAdd(CheckStaffMixin,FormView):
    form_class=MoreContentForm
    template_name="newsapp/morenewsform.html"
    def get(self, request, *args, **kwargs):
        try:
            Article.objects.get(slug=kwargs['slug'])
        except:
            messages.info(request,"article not found")
            return redirect("newsapp:Index")
        return super().get(request,*args,**kwargs)
    def form_valid(self, form):
       article=Article.objects.get(slug=self.kwargs['slug'])
       more_content=form.save(commit=False)
       more_content.article=article
       more_content.author=self.request.user
       more_content.save()
       messages.info(self.request,"more images and paragraphs added")
       return redirect("newsapp:MoreContentAdd",article.slug)

#edit news view
class UpdateArticle(CheckStaffMixin,UpdateView):
    model=Article
    form_class=ArticleUpdateForm
    template_name="newsapp/update_article.html"
    Factoryformmodel=modelformset_factory(MoreContent,form=MoreContentForm,extra=1)
    def get(self, request, *args, **kwargs):
        try:
            Article.objects.get(slug=kwargs['slug'])
        except:
            messages.info(request,"article not found")
            return redirect("newsapp:Index")
        return super().get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        formset=self.Factoryformmodel(queryset=self.get_object().morecontent_set.all())
        context['formset']=formset
        return context

    def form_valid(self, form):
        formset=self.Factoryformmodel(self.request.POST,self.request.FILES ,queryset=self.get_object().morecontent_set.all())
        form.save()
        try:
            if formset.is_valid():
                for form in formset:
                    child=form.save(commit=False)
                    child.article=self.object
                    child.author=self.request.user
                    child.save()   
            messages.info(self.request,"article updated")
            return redirect("newsapp:UpdateArticle",self.object.slug)
        except Exception as err:
            messages.info(self.request,"article failed update")
            return redirect("newsapp:UpdateArticle",self.object.slug)

#delete news view
class DeleteArticle(CheckStaffMixin,DeleteView):
    model=Article
    template_name="newsapp/delete_article.html"
    success_url=reverse_lazy("newsapp:Index")
    def delete(self,request):
        messages.info(self.request,"article deleted")
        return super().delete(request)
