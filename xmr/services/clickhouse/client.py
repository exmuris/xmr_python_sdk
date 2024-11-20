from xmr.db.client import get_database_client
from xmr.db.models.base import DsoMimTable


class ClickHouseClient:
    def __init__(self):
        self._client = None

    async def initialize(self):
        if self._client is not None:
            return

        self._client = await get_database_client()

    async def check_connection(self) -> bool:
        return await self._client.ping()

    async def dso_mim_fetch_done_files(self, table: DsoMimTable) -> set:
        ctx = self._client.create_query_context(
            **table.get_filenames_query_ctx_params()
        )
        result = await self._client.query(context=ctx)
        return set(result.result_columns[0])


# from xmr.db.models.base import *
# from xmr.services.clickhouse.client import *
# client = ClickHouseClient()
# await client.initialize()
# await client.dso_mim_fetch_done_files(Generation344())
