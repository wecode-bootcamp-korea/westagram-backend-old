#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls    import path
from posting.views import PostsView, Posts_ListView

urlpatterns = [
    path('/post', PostsView.as_view()),
    path('/post-list', Posts_ListView.as_view())
]
