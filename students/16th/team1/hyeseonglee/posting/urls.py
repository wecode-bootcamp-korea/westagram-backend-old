from django.urls import path
from posting.views  import PostView, CommentView

urlpatterns = [
    path('/create', PostView.as_view()),
    path('/read', PostView.as_view()),                      # 전체 포스트 조회기능
    path('/<int:pk>/create/comment', CommentView.as_view()),         # 댓글 생성
    path('/<int:pk>/read/comment', CommentView.as_view()),           # 댓글 조회

]
