import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Alembic Config object
config = context.config

# Configure Python logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Get SQLAlchemy engine from Flask app
def get_engine():
    try:
        # For Flask-SQLAlchemy < 3.0
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # For Flask-SQLAlchemy >= 3.0
        return current_app.extensions['migrate'].db.engine

# Get DB URL from engine
def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

# Set the SQLAlchemy URL so Alembic can use it
config.set_main_option('sqlalchemy.url', get_engine_url())

# Get the app’s metadata
target_db = current_app.extensions['migrate'].db
def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

# Handle offline migrations
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        compare_type=True  # ensure column type changes are detected
    )
    with context.begin_transaction():
        context.run_migrations()

# Handle online migrations
def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No schema changes detected.")

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            compare_type=True,  # detect column type/length changes
            **conf_args
        )
        with context.begin_transaction():
            context.run_migrations()

# Decide which mode to use
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
