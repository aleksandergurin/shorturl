from sqlalchemy import select

from app.model import short_url


async def get_url_from_db(db, url_id):
    """
    Returns url from database that correspond to specified `url_id'
    or `None' if there is no such url in database.
    """

    async with db.acquire() as conn:
        async with conn.begin():
            query = (
                select([short_url.c.url])
                .select_from(short_url)
                .where(short_url.c.id == url_id)
            )
            query_res = await conn.execute(query)
            res = await query_res.fetchone()
            if not res:
                return  # 404

            return res.url


async def put_url_into_db(db, url):
    """
    Inserts specified `url' into database if needed,
    returns id of `url' from database.
    """

    async with db.acquire() as conn:
        async with conn.begin():
            query = (
                select([short_url.c.id, short_url.c.url])
                .select_from(short_url)
                .where(short_url.c.url == url)
            )
            query_res = await conn.execute(query)
            res = await query_res.fetchone()
            if not res:
                url_id = await conn.scalar(
                    short_url.insert().values(url=url)
                )
            else:
                url_id = res.id
            return url_id
