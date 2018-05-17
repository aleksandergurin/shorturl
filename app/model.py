from sqlalchemy import (
    MetaData,
    Table,
    Column,
    BigInteger,
    Text,
)


metadata = MetaData()

short_url = Table(
    'short_url',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('url', Text),
)
