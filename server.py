import json
import os

from aiohttp import web
from aiohttp_utils import Response, routing, negotiation, run
from aiohttp_utils.negotiation import JSONRenderer

from database import session, Place, create_database
from load_data_from_csv import load_data
from statistics import Stats

app = web.Application(router=routing.ResourceRouter())


class PlaceResource:

    async def get(self, request):
        addr = request.GET.get('addr')
        if addr:
            addr = addr.replace('+', ' ')
            data = {'results': [p.to_json() for p in session().query(Place).all()]}
            s = Stats()
            res = s.get_stats(addr, data)
            return Response({'reseults': res})
        else:
            data = {'results': [p.to_json() for p in session().query(Place).all()]}
            return Response(data)

    async def post(self, request):
        path = request.GET.get('path')
        dir = 'data'
        if path:
            load_data('{}/{}'.format(dir, path))
            return Response({'result': 'loaded {}'.format(path)})

        files = os.listdir(dir)
        for file in files:
            load_data('{}/{}'.format(dir, file))
        return Response({'result': 'loaded {}'.format(' '.join(files))})


app.router.add_resource_object('/', PlaceResource())


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
