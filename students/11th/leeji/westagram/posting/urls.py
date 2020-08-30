from django.urls    import path
from .views         import Post_View,Post_List_View, Comment_List_View, Comment_View

urlpatterns = [
    path('/upload', Post_View.as_view()      ),
    path('/list',   Post_List_View.as_view() ),
    path('/<int:post_id>/upload', Comment_View.as_view() ),
    path('/<int:post_id>/list', Comment_List_View.as_view() ),
]