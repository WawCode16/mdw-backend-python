import json

from aiohttp import web

from database import create_database, session, Place


async def handle(request):
    places = session().query(Place).all()
    return web.Response(text=json.dumps({'results': [p.to_json() for p in places]}))


create_database()

app = web.Application()
app.router.add_get('/', handle)
web.run_app(app)
