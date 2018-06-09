from aiohttp import web
import aiohttp_jinja2
import bcrypt


class SignIn(web.View):
    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        return {'title': 'Sign In'}

    async def post(self):
        data = await self.request.post()
        req = self.request.app['connection']
        user_num = await req.incr('last-user-id')
        password = data.get('password').encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        await req.set("username:" + str(user_num), data.get('username'))
        await req.set("password:username:" + str(user_num), hashed)
        response = web.HTTPFound('/')
        response.set_cookie('user', data.get('username'))
        return response
