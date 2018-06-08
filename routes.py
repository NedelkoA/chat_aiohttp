from views.login import LoginView
from views.signin import SignIn
from views.index import ws_heandler


def setup_routes(app):
    #app.router.add_get('/', index_handler)
    app.router.add_get('/', ws_heandler)
    app.router.add_route('*', '/signin', SignIn)
    app.router.add_route('*', '/login', LoginView)
    app.router.add_static('/static', 'static', name='static')
