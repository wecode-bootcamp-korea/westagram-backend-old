#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls    import path
from posting.views import PostsView, CommentsView

urlpatterns =                  [
    path('',PostsView.as_view()),
    path('/<str:slug>/comments',CommentsView.as_view()),
]
