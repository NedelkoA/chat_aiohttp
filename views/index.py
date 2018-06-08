from aiohttp import web
import aiohttp


async def ws_heandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    req = request.app['connection']
    request.app['websockets'].add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(msg.data)
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
                    await req.rpush("message:4", msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('exeption')
    finally:
        request.app['websockets'].discard(ws)
    return ws