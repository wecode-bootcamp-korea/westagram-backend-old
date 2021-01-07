import json
import re

from django.http  import JsonResponse
from django.views import View

# from posting.models  import # specify models


class PostingView(View):
# if posting process 
    """
    message
    {
    user: "each-user-name" - have to validate to prevent cracking
    content: "TEXT-string"
    image_url: ["url_1", "url_2", "url_3"]
    }


    """


    def post(self, request):
        data = json.loads(request.body)
        """
        when i want to post imgs,,,
        posted_person: user-name
        article_name? no article name - generate id.


        """
    # to see all posting article whenafter posting has succeed
    # to check posting works done perfectly

class SeeArticlesView(View):
    """
    to see all articles in specific users page when someone visit there
    """
    def get(self, request):
        data = json.loads(request.body)

        """
        to display postedarticle, shall include info.
        {posted_person, article_number, posted_content, posted_date/time}
        """


        return JsonResponse({'MESSAGE': "TESTING"})
