import json, jwt, my_settings

from django.http    import JsonResponse

from users.models   import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        #login_Check
        if "Authorization" not in request.headers:
            return JsonResponse({"message" : "NEED_LOGIN"}, status=401)

        try :
            access_token    = request.headers['Authorization']
            payload         = jwt.decode(access_token, my_settings.SECRET['secret'], algorithms=my_settings.ALGORITHM)
            login_user      = Account.objects.get(email=payload['email'])
            request.account = login_user
            return func(self, request, *args, **kwargs)


        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        except Account.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

    return wrapper
