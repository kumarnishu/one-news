from django.urls import path
from . import views

app_name="newsapp"
urlpatterns=[
    # home page url
    path("",views.Index.as_view(),name="Index"),
    # articles urls
    path("article/<slug:slug>/",views.NewsDetail.as_view(),name="NewsDetail"),
    path("article/category/<slug:slug>/",views.NewsByCategory.as_view(),name="NewsByCategory"),
    path("search/",views.Search.as_view(),name="Search"),
    path("create/article",views.CreateArticle.as_view(),name="CreateArticle"),
    path("more/add/article/<slug:slug>",views.MoreContentAdd.as_view(),name="MoreContentAdd"),
    path("update/article/<slug:slug>",views.UpdateArticle.as_view(),name="UpdateArticle"),
    path("delete/article/<slug:slug>",views.DeleteArticle.as_view(),name="DeleteArticle"),
    # accounts urls
]       