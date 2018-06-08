from aiohttp import web
from routes import setup_routes
from settings import config
import aioredis
import jinja2
import aiohttp_jinja2


async def init_db(app):
    conf = app['config']['redis']
    connection = await aioredis.create_redis((conf['host'], conf['port']))
    app['connection'] = connection


async def close_redis(app):
    app['connection'].close()


async def auth_cookie_factory(app, handler):
    async def auth_cookie_handler(request):
        if request.path == '/' and request.cookies.get('user') is None:
            return web.HTTPFound('/login')
        return await handler(request)
    return auth_cookie_handler


middlewares = [auth_cookie_factory]
app = web.Application(middlewares=middlewares)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'
app.on_startup.append(init_db)
setup_routes(app)
app['config'] = config
app.on_cleanup.append(close_redis)
web.run_app(app)
