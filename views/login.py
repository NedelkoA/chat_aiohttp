import bcrypt
from aiohttp import web
import aiohttp_jinja2
import json


class LoginView(web.View):
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        if self.request.cookies.get('user'):
            return web.HTTPFound('/')
        return {'title': 'Authorization'}

    async def post(self):
        data = await self.request.post()
        req = self.request.app['connection']
        if await self.check_username(data.get('username'), req):
            if await self.check_password(data.get('password'), req):
                response = web.HTTPFound('/')
                response.set_cookie('user', data.get('username'))
                return response
            else:
                return web.Response(content_type='application/json', text=json.dumps({'error': "Wrong data"}))
        else:
            return web.Response(content_type='application/json', text=json.dumps({'error': "Wrong data"}))

    async def check_username(self, name, req):
        users_key = await req.keys('username:*')
        name = name.encode('utf-8')
        for key in users_key:
            user = await req.get(key)
            if user == name:
                return True

    async def check_password(self, pas, req):
        password_key = await req.keys('password:username:*')
        pas = pas.encode('utf-8')
        for key in password_key:
            password = await req.get(key)
            if bcrypt.checkpw(pas, password):
                return True
