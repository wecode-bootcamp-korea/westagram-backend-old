import json

from django.views   import View
from django.http    import JsonResponse

from .models        import PostMedia, Photo, Comment
from user.models    import User
from .utils         import authorization    
class PostingView(View):   
    @authorization
    def post(self, request, user_id):
            data                 = json.loads(request.body)
            login_user           = User.objects.get(id= user_id)
            posting              = PostMedia.objects.create(
                
                title            = data['title'],
                content          = data['content'],
                user_id          = login_user.id
            )

            image_URLs  = data['image']
            for image in image_URLs:
                Photo.objects.create(
                    post_id      = posting.id,
                    image        = image
                )
            return JsonResponse({'message':'SUCCESS'}, status=200)

    @authorization
    def get(self, request, user_id):
        login_user               = User.objects.get(id= user_id)
        posted_data              = PostMedia.objects.get(user_id= user_id)
        posted_image             = Photo.objects.filter(post_id= posted_data.id)
        
        data_dict                = {}
        data_dict['user_name']   = login_user.name
        data_dict['post_id']     = posted_data.id   
        data_dict['title']       = posted_data.title
        data_dict['content']     = posted_data.content

        image_list               = []
        for img in posted_image:
            image_list.append(img.image) 
        return JsonResponse({'posted_data':data_dict, 'posted image':image_list}, status=200)
class CommentView(View):
    def post(self, request):
        #post id도 일단 데이터로 받는다.
        data = json.loads(request.body)
        content = data.get('content')
        re_comment_id = data.get('re_comment_id')

        if content == None:
            return JsonResponse({'message':'EMPTY_CONTENT'}, status= 400)
        Comment.objects(
            content = data['content'],
            post_id = data['post_id']
            re_comment_id = data['comment_id'] if not recomment_id else None
        ).save

# class ReCommentView(View):
#     def post(self, request):
#         #post id도 일단 데이터로 받는다.
#         data = json.loads(request.body)
#         content = data.get('content')

#         if content == None:
#             return JsonResponse({'message':'EMPTY_CONTENT'}, status= 400)
#         Comment.objects(
#             content = data['content'],
#             post_id = data['post_id'],
#             re_comment_id = data['comment_id']
#         ).save




