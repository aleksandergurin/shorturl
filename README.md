REST service for URL shortening.

Required python version 3.6, aiohttp, aiopg, sqlalchemy.

To run service you need PostgreSQL database (default URL:
postgresql://postgres:postgres@localhost:5432
you can run database inside docker container with command
`sudo docker run --name postgres -p 5432:5432 -d postgres`).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
python3 -m app
```


API:

```
PUT  http://zakup.co/?url=ENCODED_URL
GET  http://zakup.co/SHORT_URL
```


CLI EXAMPLE:

```bash
curl -X PUT -G localhost:8080 --data-urlencode 'url=http://example.com'
curl -I -X GET localhost:8080/4GFfc4
```
