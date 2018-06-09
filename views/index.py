from aiohttp import web
import aiohttp
import aiohttp_jinja2


async def ws_heandler(request):
    current_name = request.cookies['user']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    req = request.app['connection']
    request.app['websockets'].append(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                message_num = await req.incr('last-message-id')
                web.HTTPFound('/')
                await req.set("message:" + str(message_num), msg.data)
                await req.set("user:message:" + str(message_num), current_name)
                for ws in request.app['websockets']:
                    await ws.send_json({'text': msg.data, 'name': current_name})
    finally:
        request.app['websockets'].remove(ws)
    return ws


@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    req = request.app['connection']
    current_name = request.cookies['user']
    count_message = await req.get('last-message-id')
    messages = []
    num_msg = int(count_message.decode('utf-8')) + 1
    for each in range(1, num_msg):
        message = await req.get('message:' + str(each))
        user = await req.get('user:message:' + str(each))
        messages.append(
            (
                user.decode('utf-8'),
                message.decode('utf-8')
            ))
    return {'title': 'Chat', 'messages': messages, 'current_name': current_name}


async def logout_handler(request):
    response = web.HTTPFound('/login')
    response.del_cookie('user')
    return response
