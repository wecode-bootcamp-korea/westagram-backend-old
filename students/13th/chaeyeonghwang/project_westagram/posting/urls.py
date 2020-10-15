from django.urls import path
from posting.views import UploadView, ShowView, UploadCommentView, ShowCommentView, LikeView, DeleteView, DeleteCommentView,  UpdateView, ReplyView

urlpatterns = [
    path('postingupload', UploadView.as_view()),
    path('postingshow',   ShowView.as_view()),
    path('commentupload', UploadCommentView.as_view()),
    path('commentshow',   ShowCommentView.as_view()),
    path('like',          LikeView.as_view()),
    path('postingdelete', DeleteView.as_view()),
    path('commentdelete', DeleteCommentView.as_view()),
    path('update',        UpdateView.as_view()),
    path('reply',         ReplyView.as_view())
]
