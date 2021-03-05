from django.urls import path
from .views      import UserListView, Dog view

urlpatterns = [
    path('', UserListView.as_view()), 
    path('/dog', DogView.as_view())
]
