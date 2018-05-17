from urllib import parse

from aiohttp import web

from app.errors import not_found
from app.queries import (
    get_url_from_db,
    put_url_into_db,
)
from app.bl import (
    to_base,
    from_base,
)
from app.consts import (
    URL_QUERY_PARAM,
    URL_ID_PARAM,
    DB,
)


async def get_url(request):
    url_id = request.match_info.get(URL_ID_PARAM)
    if not url_id:
        return not_found()

    url_id = from_base(url_id)
    if url_id == -1:
        return not_found()

    url = await get_url_from_db(request.app[DB], url_id)
    if not url:
        return not_found()

    return web.Response(
        status=302,
        headers={
            'Location': url,
            'Content-Type': 'text/html; charset=UTF-8',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
        }
    )


async def put_url(request):
    encoded_url = request.query.get(URL_QUERY_PARAM)
    if not encoded_url:
        return not_found()

    url_id = await put_url_into_db(
        request.app[DB], parse.unquote(encoded_url)
    )

    return web.Response(
        status=200,
        text=f'{request.scheme}://{request.host}/{to_base(url_id)}',
    )
