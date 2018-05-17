import asyncio
from collections import namedtuple
import logging

from aiohttp import web
from aiohttp_middlewares import timeout_middleware
from aiopg.sa import create_engine

from app.config import make_parser
from app.errors import error
from app.views import (
    get_url,
    put_url,
)
from app.consts import (
    URL_ID_PARAM,
    DB,
    CONF,
)

log = logging.getLogger(__name__)


def error_middleware(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                if not response:
                    override = overrides.get(500)
                    return override(request, response)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return override(request, response)
            except asyncio.TimeoutError as ex:
                log.exception(
                    'Timeout error',
                    extra={
                        'request': request.method,
                        'url': str(request.rel_url),
                    }
                )
                override = overrides.get(504)
                return override(request, ex)
            except web.HTTPException as ex:
                log.exception(
                    'HTTP exception',
                    extra={
                        'request': request.method,
                        'url': str(request.rel_url),
                    }
                )
                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return override(request, ex)
            except Exception as ex:
                log.exception(
                    'Exception',
                    extra={
                        'request': request.method,
                        'url': str(request.rel_url),
                    }
                )
                override = overrides.get(500)
                return override(request, ex)
        return middleware_handler
    return middleware


async def connect_db(app: web.Application) -> None:
    conf = app[CONF]
    app[DB] = await create_engine(
        host=conf.db_host,
        database=conf.db_name,
        port=conf.db_port,
        user=conf.db_user,
        password=conf.db_password,
    )
    log.info('Connected to database')


async def disconnect_db(app: web.Application) -> None:
    db = app[DB]
    db.close()
    await db.wait_closed()
    log.info('Disconnected from database')


def create_app(timeout, db_host, db_name, db_port, db_user, db_password):
    app = web.Application()

    conf = namedtuple('conf', [
        'db_host', 'db_name', 'db_port', 'db_user', 'db_password',
    ])
    conf.db_host = db_host
    conf.db_name = db_name
    conf.db_port = db_port
    conf.db_user = db_user
    conf.db_password = db_password

    app[CONF] = conf

    # Signal handlers
    app.on_startup.extend([
        connect_db,
    ])
    app.on_cleanup.extend([
        disconnect_db,
    ])

    # Middleware
    app.middlewares.extend([
        error_middleware({
            404: lambda req, resp: error(404),
            500: lambda req, resp: error(500),
            504: lambda req, resp: error(504),
        }),
        timeout_middleware(timeout),
    ])

    # Routes
    app.router.add_get('/{%s}' % URL_ID_PARAM, get_url)
    app.router.add_put('/', put_url)

    return app


def main():
    args = make_parser().parse_args()
    web.run_app(
        create_app(
            args.timeout,
            args.db_host,
            args.db_name,
            args.db_port,
            args.db_user,
            args.db_password,
        ),
        host=args.host,
        port=args.port,
    )


if __name__ == '__main__':
    main()
