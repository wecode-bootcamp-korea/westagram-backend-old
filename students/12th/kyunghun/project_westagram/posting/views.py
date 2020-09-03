import json

from django.views   import View
from django.http    import JsonResponse

from .models        import PostMedia, Photo
from user.models    import Users
    
class PostingView(View):   
    def post(self, request):
            data                 = json.loads(request.body)
            login_user           = Users.objects.get(email = data['email'])
            login_user_id        = login_user.id
            posting              = PostMedia.objects.create(
                
                title            = data['title'],
                content          = data['content'],
                user_id          = login_user_id
            )
            Photo.objects.create(
                post_id          = posting.id,
                image            = data['img']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        data                     = json.loads(request.body)
        login_user               = Users.objects.get(email = data['email'])
        login_user_id            = login_user.id
        
        posted_data              = PostMedia.objects.get(user_id= login_user_id)
        posted_image             = Photo.objects.filter(post_id= posted_data.id)
        
        data_dict                = {'user_name':login_user.name}
        image_list               = []
        data_dict['title']       = posted_data.title
        data_dict['content']     = posted_data.content

        for img in posted_image:
            image_list.append(img.image) 
        return JsonResponse({'posted_data':data_dict, 'posted image':image_list}, status=200)

