import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
import sys
sys.path.append(sys_path)
from app.models.base import Base  # noqa: E402

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DB driver to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        context.config.attributes.get("connection", None) or
        context.config.get_section_option(context.config.config_ini_section, "sqlalchemy.url")
    )

    async def do_run_migrations(connection: Connection) -> None:
        await connection.run_sync(do_run_migrations_sync)

    async def do_run_migrations_sync(sync_connection):
        context.configure(
            connection=sync_connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    import asyncio
    asyncio.run(_run_async(engine))

async def _run_async(engine):
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations_sync)
    await engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()