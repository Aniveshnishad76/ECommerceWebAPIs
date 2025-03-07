from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from src.schema.schema import Base

from src.config.env import get_settings
app_config = get_settings()
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USERNAME", app_config.db_app.db_username)
config.set_section_option(section, "DB_PASSWORD", app_config.db_app.db_password)
config.set_section_option(section, "DB_NAME", app_config.db_app.db_name)
config.set_section_option(section, "DB_HOST", app_config.db_app.db_host)

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def get_url():
    """DB string"""
    return "postgresql://%s:%s@%s/%s" % (
        app_config.db_app.db_username,
        app_config.db_app.db_password,
        app_config.db_app.db_host,
        app_config.db_app.db_name,
    )

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=get_url(),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
