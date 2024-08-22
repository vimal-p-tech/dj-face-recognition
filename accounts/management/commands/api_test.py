from django.core.management.base import BaseCommand
import requests
from django.http import JsonResponse
from accounts.api.blog_service import API

class Command(BaseCommand):
    help = 'My custom command description'

    def handle(self, *args, **options):
        # response = requests.get('http://localhost:8002/blog/blogposts/')
        # print("response",response.json())
        url = "http://localhost:8002/blog/blogposts/"
        jwt_token = "sdkjfk"
        api_obj = API(url,jwt_token)
        response = api_obj.call()
        print(response)

        return JsonResponse(response,safe=False)
        # self.stdout.write(self.style.SUCCESS('Custom command executed successfully'))