import clickhouse_connect


async def get_database_client():
    # replace with config env vars
    return await clickhouse_connect.get_async_client(
        host="localhost",
        username="default",
        database="pinergy",
        autogenerate_session_id=False,
    )
