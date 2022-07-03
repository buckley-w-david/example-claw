import os
from flask import Flask

from example_claw.discord import discord

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['DISCORD_PUBLIC_KEY'] = os.environ['DISCORD_PUBLIC_KEY']
    app.config['DISCORD_CLIENT_ID'] = os.environ['DISCORD_CLIENT_ID']
    app.config['DISCORD_CLIENT_SECRET'] = os.environ['DISCORD_CLIENT_SECRET']
    discord.init_app(app)
    return app
