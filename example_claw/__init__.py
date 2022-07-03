from typing import cast, List
import os
from flask_discord_interactions import Discord
from flask_discord_interactions import discord_types as types
from flask import Flask

discord = Discord()

import random

with open('prefix.txt', 'r') as f:
    prefix = [l.strip() for l in f.readlines()]

with open('suffix.txt', 'r') as f:
    suffix = [l.strip() for l in f.readlines()]

@discord.command("names")
def names(interaction: types.ChatInteraction) -> types.InteractionResponse:
    names = []

    if (options := interaction.data.options):
        value = int(options[0].value) 
    else:
        value = 5

    for _ in range(value):
        names.append(f"{random.choice(prefix).capitalize()}{random.choice(suffix).lower()}")

    return types.InteractionResponse(
        type=types.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=types.InteractionCallbackDataMessages(
            content="\n".join(names),
        )
    )
names.description = "Generate names"

arg = types.ApplicationCommandOption(
    type=types.ApplicationCommandOptionType.INTEGER,
    name="number",
    description="The number of names to generate",
    required=False,
    min_value=1,
    max_value=10,
)
names.add_option(arg)

app = Flask(__name__)
app.config['DISCORD_PUBLIC_KEY'] = os.environ['DISCORD_PUBLIC_KEY']
app.config['DISCORD_CLIENT_ID'] = os.environ['DISCORD_CLIENT_ID']
app.config['DISCORD_CLIENT_SECRET'] = os.environ['DISCORD_CLIENT_SECRET']

discord.init_app(app)
