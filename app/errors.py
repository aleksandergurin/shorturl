from aiohttp import web

ERRORS = {
    404: 'Not found',
    500: 'Internal Server Error',
    504: 'Timeout error'
}


def not_found():
    return error(404)


def error(code: int) -> web.Response:
    return web.Response(
        status=code,
        text='{} {}'.format(code, ERRORS.get(code, 'Error')),
        headers={
            'Content-Type': 'text/html; charset=UTF-8',
            'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
        }
    )
