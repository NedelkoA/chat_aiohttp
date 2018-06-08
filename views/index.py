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
            else:
                break
    finally:
        request.app['websockets'].remove(ws)
    return ws


@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    req = request.app['connection']
    count_message = await req.get('last-message-id')
    messages = []
    for i in range(1, int(count_message.decode('utf-8')) + 1):
        message = await req.get('message:' + str(i))
        user = await req.get('user:message:'+ str(i))
        messages.append(
            (
                message.decode('utf-8'),
                user.decode('utf-8')
            )
        )

    return {'title': 'Chat', 'messages': messages}
