from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

backend_root = Path(__file__).resolve().parents[1]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

target_metadata = None


def run_migrations_offline() -> None:
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
    raise RuntimeError(
        "Alembic online migrations require database models and an engine, "
        "which are outside the scope of this foundation task."
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
