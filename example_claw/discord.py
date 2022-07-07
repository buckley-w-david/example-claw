import random
from typing import cast, List

from flask_discord_interactions import Discord
from flask_discord_interactions import discord_types as types

discord = Discord()

with open('prefix.txt', 'r') as f:
    prefix = [l.strip() for l in f.readlines()]

with open('suffix.txt', 'r') as f:
    suffix = [l.strip() for l in f.readlines()]

@discord.command("names")
def names(interaction: types.ChatInteraction) -> types.InteractionResponse:
    names = []

    if (options := interaction.data.options):
        value = int(options[0].value) # type: ignore
    else:
        value = 10

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
