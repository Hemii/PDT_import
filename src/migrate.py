from sqlalchemy import MetaData
from sqlalchemy.schema import DropTable
from src.connection import engine, Base
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet


DO_NOT_DROP = ['spatial_ref_sys']

def drop_tables(engine,exclude_tables):
    meta = MetaData(engine)
    meta.reflect(bind=engine)
    connection = engine.connect()

    for tbl in reversed(meta.sorted_tables):
        if tbl.name not in exclude_tables:
            connection.execute(DropTable(tbl))


drop_tables(engine, DO_NOT_DROP)

Base.metadata.create_all(engine)