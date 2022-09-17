from django.middleware.common import CommonMiddleware


class MyCustomMiddleWare(CommonMiddleware):
    def process_request(self, request):
        if not request.path.endswith('/'):
            request.path_info = request.path_info + '/'

        return None
