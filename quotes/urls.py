from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name="main"),
    path('<int:page>/', views.main, name="main_paginate"),
    path('author/<str:author_name>/', views.author, name='author'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('tag/<str:tag_name>/<int:page>/', views.tag, name='tag_paginate'),
    path('add/author/', views.AddAuthorView.as_view(), name='add_author'),
    path('add/tag/', views.AddTagView.as_view(), name='add_tag'),    
    path('add/quote/', views.AddQuoteView.as_view(), name='add_quote'),
]