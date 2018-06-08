import bcrypt
from aiohttp import web
import aiohttp_jinja2


class LoginView(web.View):
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        if self.request.cookies.get('user'):
            return web.HTTPFound('/')
        return {'title': 'Authorization'}

    async def post(self):
        data = await self.request.post()
        req = self.request.app['connection']
        number_of_users = await req.get('last-user-id')
        for i in range(1, int(number_of_users.decode('utf-8')) + 1):
            user = await req.get('username:' + str(i))
            if user.decode('utf-8') == data.get('username'):
                password = await req.get('password:username:' + str(i))
                if bcrypt.checkpw(data.get('password').encode('utf-8'), password):
                    response = web.HTTPFound('/')
                    response.set_cookie('user', data.get('username'))
                    return response
