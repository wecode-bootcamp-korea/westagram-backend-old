from django.urls import path
from posting.views  import PostView, PostCommentView,PostLikeView

urlpatterns = [
    path('/create', PostView.as_view()),
    path('/read', PostView.as_view()),                              # 전체 포스트 조회기능
    path('/create/<int:pk>/comment', PostCommentView.as_view()),   # 댓글 생성
    path('/read/<int:pk>/comment', PostCommentView.as_view()),     # 댓글 조회
    
    path('/create/<int:pk>/like', PostLikeView.as_view()),           # 좋아요 등록
    path('/read/<int:pk>/like', PostLikeView.as_view()),            # 좋아요 조회


]
