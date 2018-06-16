import tornado.ioloop
import tornado.web
from qrcode import empower
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url, lgToken, umid_token = empower()
        r.lpush("token", (lgToken, umid_token))
        self.redirect(url, permanent=True)
        
        
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
 
        