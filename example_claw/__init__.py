import os
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
    app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
    app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]

    from example_claw.discord import discord

    discord.init_app(app)

    from example_claw import admin

    app.register_blueprint(admin.bp)

    from example_claw import database

    database.init_db(app)

    app.secret_key = os.environ['EXAMPLE_CLAW_SECRET_KEY']

    return app
