from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class MiddleWareTest(MiddlewareMixin):
    def process_request(self,request):
        request_ip = request.META["REMOTE_ADDR"]
        print(request_ip)