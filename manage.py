from flask.cli import FlaskGroup
from app.__init__ import create_app
from app.extensions import db

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
