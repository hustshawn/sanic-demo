from sanic.response import json, text
from sanic import Blueprint

bp_cookie = Blueprint('cookie_blueprint', url_prefix='/cookie')

@bp_cookie.route('/')
async def bp_root(request):
    return json({'Bluprint': 'cookie'})

@bp_cookie.route('/set')
async def set_cookie(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response

@bp_cookie.route('/get')
async def get_cookie(request):
    test_cookie = request.cookies.get('test')
    return text("Test cookie set to: {}".format(test_cookie))

from sanic.views import HTTPMethodView
class CookieView(HTTPMethodView):
    async def get(self, request):
        return text('This is async get method.')

    def post(self, request):
        pass

bp_cookie.add_route(CookieView.as_view(), '/cls')
