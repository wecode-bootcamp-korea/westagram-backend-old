import json
import io
from PIL              import Image

from django.views     import View
from django.http      import JsonResponse
from django.db        import IntegrityError, transaction

from user.models      import User
from post.models      import Post, PostImage, Comment
from post.exceptions  import (
    BlankFieldException,
    ImageUploadFailException,
    PostUploadFailException
)
from post.validations import Validation
from common_util.authorization import check_valid_user

class PostListAll(View):
    
    def get(self, request):
        data = json.loads(request.body)
        try:
            get_number_of_post = data["get_number_of_post"]
            
            # TODO:Paging
            posts = Post.objects.filter(is_deleted=0)[:get_number_of_post]
            
            post_list = {
                "count": len(posts),
                "posts": [{
                    "post_key"      : post.post_key,
                    "post_desc"     : post.post_desc,
                    "tags"          : post.tags,
                    "location_info" : post.location_info,
                    "updated_at"    : post.updated_at,
                    "user"          : post.user.name,
                    "user_name"     : post.user.user_name,
                    } for post in posts]
            }
            
            return JsonResponse({"get": post_list}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except AttributeError:
            return JsonResponse({"message": "ATTRIBUTE_ERROR"}, status=400)

class PostList(View):
    
    @check_valid_user
    def post(self, request):
        user_id = request.user.id
        try:
            if Validation.is_blank(user_id):
                raise BlankFieldException
            
            user  = User.objects.get(id=user_id, is_deleted=0)
            posts = user.post_set.all()
            post_list = []
            if posts:
                post_list = [
                    {
                        "post_key"     : post.post_key,
                        "post_desc"    : post.post_desc,
                        "updated_at"   : post.updated_at,
                        "first_img_url":
                            post.postimage_set.all().first().img_url,
                        "comments"     : [{
                            "comment"   : comment.comment,
                            "updated_at": comment.updated_at,
                            "user"      : comment.user.user_name
                        } for comment in post.comment_set.all()]
                    }
                    for post in posts
                ]
            
            result = {
                user.user_name: {
                    "posts": post_list
                }
            }
            
            return JsonResponse({"post": result}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except AttributeError:
            return JsonResponse({"message": "ATTRIBUTE_ERROR"}, status=400)

class PostUp(View):
    
    def get(self, request):
        return JsonResponse({"get": "post up"}, status=200)
    
    @transaction.atomic
    @check_valid_user
    def post(self, request):
        try:
            print("end check::=======", request.POST['user_id'])
            
            user_id   = request.POST['user_id']
            post_desc   = request.POST['post_desc']
            post_images = request.FILES.getlist('post_images')
            
            if Validation.is_blank(user_id, post_images):
                raise BlankFieldException
            
            if not post_images:
                raise ImageUploadFailException
            
            user = User.objects.get(id=user_id)
            post = Post(
                post_desc = post_desc.strip(),
                user      = user
            )
            
            if not post:
                raise PostUploadFailException
            else:
                post.save()
                
                post_imgs = []
                AMAZON_STORAGE_URL = "/amazon/storage/" + user.user_name
                
                for image in post_images:
                    img_byte_arr = io.BytesIO()
                    img          = Image.open(image, mode='r')
                    img.save(img_byte_arr, format=img.format)
                    
                    # TODO: restore to AMAZON STORAGE
                    img_binary = img_byte_arr.getvalue()
                    
                    post_img = PostImage(
                        img_name   = str(image),
                        img_url    = AMAZON_STORAGE_URL + "/" + str(image),
                        img_format = img.format,
                        img_size   = img_binary.__sizeof__(),
                        post       = post
                    )
                    
                    if not post_img:
                        raise Exception("이미지 정보 추출 중 에러가 발생하였습니다.")
                    else:
                        post_imgs.append(post_img)
                    
                try:
                    with transaction.atomic():
                        for p_img in post_imgs:
                            p_img.save()

                except IntegrityError:
                    return JsonResponse(
                        {"message": "Transaction Error"}, status=400)
            
            return JsonResponse({"post": "post upload success"}, status=201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except AttributeError:
            return JsonResponse({"message": "ATTRIBUTE_ERROR"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except ImageUploadFailException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except PostUploadFailException as e:
            return JsonResponse({"message": e.__str__()}, status=400)

class PostLike(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            post_id = data['post_id']

            likes = Post.objects.select_related('like_posts').all()
            
            print(likes)
            
            
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        return JsonResponse({"message": "SUCCESS"}, status=200)

# ============================================================================
# comment 기능
class GetAllComments(View):
    
    def get(self, request):
        data = json.loads(request.body)
        try:
            num          = data['get_comments_num']
            all_comments = Comment.objects.all().filter(is_deleted=0)[:num]
            
            comment_to_100 = [{}]
            result = {"comments_num": 0, "comments": []}
            
            if all_comments:
                comment_to_100 = [{
                    "post_key"     : comment.post.post_key,
                    "user_id"      : comment.user.pk,
                    "comment"      : comment.comment,
                    "created_date" : comment.created_at,
                    "updated_at"   : comment.updated_at,
                } for comment in all_comments]
                
                result["comments_num"] = len(all_comments)
                result["comments"]     = comment_to_100
            
            return JsonResponse({"comments": result}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except AttributeError:
            return JsonResponse({"message": "ATTRIBUTE_ERROR"}, status=400)

class AddComment(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            post_key     = data["post_key"]
            user_id      = data["user_id"]
            user_name    = data["user_name"].strip()
            user_comment = data["comment"].strip()
            
            user = User.objects.get(
                id         = user_id,
                user_name  = user_name,
                is_deleted = 0
            )
            
            post = Post.objects.get(post_key=post_key, is_deleted=0)
            
            Comment.objects.create(
                comment = user_comment,
                post    = post,
                user    = user
            )
            
            return JsonResponse({"post": "SUCCESS"}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except AttributeError:
            return JsonResponse({"message": "ATTRIBUTE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "USER NOT EXIST"}, status=400)
            
        except Post.DoesNotExist:
            return JsonResponse({"message": "POST NOT EXIST"}, status=400)