from aiohttp import web
from aiohttp_utils import Response, routing, negotiation, run

from database import session, Place

app = web.Application(router=routing.ResourceRouter())


class PlaceResource:

    async def get(self, request):
        return Response({
            'results': [p.to_json() for p in session()   .query(Place).all()]
        })


app.router.add_resource_object('/', PlaceResource())

# Content negotiation
negotiation.setup(
    app, renderers={
        'application/json': negotiation.render_json
    }
)

if __name__ == '__main__':
    # Development server
    run(
        app,
        app_uri='server:app',
        reload=True,
        host='0.0.0.0',
        port=8080
    )
