from wsgiref.simple_server import make_server
from views import router
import os, pickle, hashlib

def get_url(environ):
    query_str = environ['QUERY_STRING']
    path = environ['PATH_INFO']
    if query_str:
        path += "?" + query_str
    return path

def create_folder(name):
    try:
        os.stat(name)
    except:
        os.mkdir(name)

def caching_middleware(app):
    def wrapped_app(environ, start_response):
        url = get_url(environ)
        h = hashlib.new("ripemd160")
        h.update(url)
        hex_digest = h.hexdigest()
        cache_folder = "cache_save"
        create_folder(cache_folder)
        path_to_cache = os.path.join(cache_folder, hex_digest)
        if url == "/cache_reset":
            for name in os.listdir(cache_folder):
                os.remove(os.path.join(cache_folder, name))
        if os.path.exists(os.path.join(cache_folder, hex_digest)):
            response = app(environ, start_response)
            return pickle.load(open(path_to_cache, "rb"))
        else:
            response = app(environ, start_response)
            pickle.dump(response, open(path_to_cache, "wb"))
            return response
    return wrapped_app
if __name__ == '__main__':
    make_server('', 8000, caching_middleware(router)).serve_forever()
