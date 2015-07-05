from util import controller, Response, Router
import random, string, os

@controller
def index(request):
    return Response(200, "It works!")

@controller
def hello(request):
    name = request.GET.get('name', ["Anonymous"])[0]
    return Response(200, "Hello %s" % name)

@controller
def random_str(request):
    return Response(200, ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16)))

@controller
def cache_reset(request):
    return Response(200, "Ok")

router = Router({
    '/index': index,
    '/hello': hello,
    '/random_str': random_str,
    '/cache_reset': cache_reset,
})
