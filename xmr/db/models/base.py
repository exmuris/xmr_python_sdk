class DsoMimTable:
    def get_filenames_query_ctx_params(self) -> dict:
        return {
            "query": (
                "SELECT distinct(concat({filename:Identifier},'.xml')) "
                "FROM {tablename:Identifier}"
            ),
            "parameters": {
                "filename": self.Meta.filename_column,
                "tablename": self.Meta._tablename,
            },
        }


class Generation344(DsoMimTable):
    class Meta:
        _tablename: str = "generation344"
        filename_column: str = "filename"


# from xmr.db.models.base import *
# from xmr.services.clickhouse.client import *
# client = ClickHouseClient()
# await client.initialize()
# ctx = client._client.create_query_context(**Generation344.get_filenames_query_ctx_params())
# result = await client._client.query(**Generation344.get_filenames_query_ctx_params())
