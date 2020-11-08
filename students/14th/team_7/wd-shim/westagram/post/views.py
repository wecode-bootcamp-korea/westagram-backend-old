import json
import io
from PIL import Image

from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError, transaction

from user.models import User
from post.models import Post, PostImage
from post.exceptions import BlankFieldException
from post.validations import Validation

class PostIndex(View):
    def get(self, request):
        return JsonResponse({"get": "post index"}, status=200)

class PostListAll(View):
    def get(self, request):
        pass

class PostList(View):
    def get(self, request):
        data = json.loads(request.body)
        
        try:
            user_name = data['user_name']
            User.objects.get(user_name=user_name)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except Exception as e:
            return JsonResponse({"message": "UNKNOWN_ERROR"}, status=400)
        
        return JsonResponse({"post": "SUCCESS"}, status=200)

class PostUp(View):
    def get(self, request):
        return JsonResponse({"get": "post up"}, status=200)
    
    @transaction.atomic
    def post(self, request):
        try:
            user_name   = request.POST['user']
            post_desc   = request.POST['post_desc']
            post_images = request.FILES.getlist('post_images')
            
            if Validation.is_blank(user_name):
                raise BlankFieldException
            
            user = User.objects.get(user_name=user_name)
            post = Post(
                post_desc=post_desc.strip(),
                user=user
            )
            
            if not post:
                raise Exception("Post 객체가 정상적으로 생성 안됐음")
            else:
                post_imgs = []
                AMAZON_STORAGE_URL = "/amazon/storage/" + user.user_name
                
                for image in post_images:
                    img          = Image.open(image, mode='r')
                    img_byte_arr = io.BytesIO()
                    img.save(
                        img_byte_arr,
                        format = img.format
                    )
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
                        raise Exception("이미지 정보 추출 오류 발생!")
                    else:
                        post_imgs.append(post_img)
                
                try:
                    with transaction.atomic():
                        post.save()
                        for p_img in post_imgs:
                            p_img.save()
                
                except IntegrityError as e:
                    return JsonResponse(
                        {"message": "Transaction Error"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except Exception as e:
            return JsonResponse({"message": "UNKNOWN_ERROR"}, status=400)
        
        return JsonResponse({"post": "SUCCESS"}, status=200)