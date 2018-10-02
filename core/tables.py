import rethinkdb as r
import logging

logger = logging.getLogger("highlightpy.core.tables")
# Defines the logger.


async def create_tables(connection):
    """Creates all of the tables."""
    dbs = await r.db_list().run(connection)

    if "highlightpy" not in dbs:
        logger.info("Creating database.")
        await r.db_create("highlightpy").run(connection)

    connection.use("highlightpy")

    tables = await r.table_list().run(connection)

    if "highlightpy_word" not in tables:
        logger.info("Creating word highlight table.")
        await r.table_create("highlightpy_word").run(connection)
        await r.table("highlightpy_word").index_create(
            "guild_id").run(connection)
        await r.table("highlightpy_word").index_create(
            "user_id").run(connection)

    if "highlightpy_regex" not in tables:
        logger.info("Creating regex highlight table.")
        await r.table_create("highlightpy_regex").run(connection)
        await r.table("highlightpy_regex").index_create(
            "guild_id").run(connection)
        await r.table("highlightpy_regex").index_create(
            "user_id").run(connection)
