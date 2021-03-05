from django.urls import path
from .views      import PostManage

urlpatterns = [
    path('', PostManage.as_view())
]