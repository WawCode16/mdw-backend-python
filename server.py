import json
import os

from aiohttp import web
from aiohttp_utils import Response, routing, negotiation, run
from aiohttp_utils.negotiation import JSONRenderer

from database import session, Place, create_database
from load_data_from_csv import load_data
from statistics import Stats

app = web.Application(router=routing.ResourceRouter())


class CORSResponse(Response):
    def __init__(self, *args, **kwargs):
        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers']['Access-Control-Allow-Origin'] = '*'
        super().__init__(*args, **kwargs)


class PlaceResource:

    async def get(self, request):
        off = int(request.GET.get('offset', 0))
        per_page = int(request.GET.get('limit', 20))
        data = {
            'offset': off,
            'limit': per_page,
            'next': '?offset={}&limit={}'.format(off + per_page, per_page),
            'results': [p.to_json() for p in session().query(Place).offset(off).limit(per_page).all()]
        }
        return CORSResponse(data)

    async def post(self, request):
        path = request.GET.get('path')
        dir = 'data'
        if path:
            load_data('{}/{}'.format(dir, path))
            return Response({'result': 'loaded {}'.format(path)})

        files = os.listdir(dir)
        for file in files:
            load_data('{}/{}'.format(dir, file))
        return CORSResponse({'result': 'loaded {}'.format(' '.join(files))})


class StatsResource:

    async def get(self, request):
        addr = request.GET.get('addr')
        res = {'stats': None}
        if addr:
            addr = addr.replace('+', ' ')
            data = {'results': [p.to_json() for p in session().query(Place).all()]}
            s = Stats()
            res = s.get_stats(addr, data)
        return CORSResponse({'stats': res})


app.router.add_resource_object('/', PlaceResource())
app.router.add_resource_object('/stats', StatsResource())


class CustomJSONRenderer(JSONRenderer):
    json_module = json


# Content negotiation
negotiation.setup(app, renderers={
        'application/json': CustomJSONRenderer()
    }
)

if __name__ == '__main__':
    # Create database
    create_database()
    # Development server
    run(
        app,
        app_uri='server:app',
        reload=True,
        host='0.0.0.0',
        port=8080
    )
