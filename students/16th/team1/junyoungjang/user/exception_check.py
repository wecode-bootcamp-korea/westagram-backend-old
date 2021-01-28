import json

from django.http import JsonResponse

def exception_check(func):
    def exception_check_func(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            return func(self, request, *args, **kwargs)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)
    return exception_check_func