from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def init_app(app: Flask):
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

from example_claw import create_app
app = create_app()
init_app(app)
