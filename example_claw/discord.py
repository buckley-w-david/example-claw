from typing import Optional, List, cast

from discord_interactions_flask import Discord
from discord_interactions_flask import interactions
from discord_interactions_flask import discord_types as types
from discord_interactions_flask.helpers import content_response


import example_claw
from example_claw.database import query_db

import importlib.resources as pkg_resources
prefix_corpus = [
    line for l in pkg_resources.read_text(example_claw, "prefix.txt").split("\n") if (line := l.strip().lower())
]
suffix_corpus = [
    line for l in pkg_resources.read_text(example_claw, "suffix.txt").split("\n") if (line := l.strip().lower())
]

discord = Discord()


def random_names(n: int, *, prefix: Optional[str] = None, suffix: Optional[str] = None) -> list[str]:
    if not prefix:
        prefixes = [row["prefix"] for row in query_db('SELECT prefix FROM prefixes WHERE id IN (SELECT id FROM prefixes ORDER BY RANDOM() LIMIT ?)', (n,))] # type: ignore
    else:
        prefixes = [prefix]*n
    if not suffix:
        suffixes = [row["suffix"] for row in query_db('SELECT suffix FROM suffixes WHERE id IN (SELECT id FROM suffixes ORDER BY RANDOM() LIMIT ?)', (n,))] # type: ignore
    else:
        suffixes = [suffix]*n

    return [f"{prefix.capitalize()}{suffix.lower()}" for (prefix, suffix) in zip(prefixes, suffixes)] # type: ignore


with discord.command("generate") as command:
    command.description = "Special name generation"

    @command.subcommand("suffixes", "Generate suffixes to go with a chosen prefix.")
    def suffixes(interaction: interactions.ChatInteraction) -> types.InteractionResponse:
        options = cast(List, interaction.data.options)[0].options
        prefix = options[0].value
        if len(options) > 1:
            value = int(options[1].value)
        else:
            value = 10

        names = random_names(value, prefix=prefix)
        return content_response("\n".join(names))

    @command.subcommand("prefixes", "Generate prefixes to go with a chosen suffix.")
    def prefixes(interaction: interactions.ChatInteraction) -> types.InteractionResponse:
        options = cast(List, interaction.data.options)[0].options
        suffix = options[0].value
        if len(options) > 1:
            value = int(options[1].value)
        else:
            value = 10

        names = random_names(value, suffix=suffix)

        return content_response("\n".join(names))

    suffixes.add_option(
        types.ApplicationCommandOption(
            type=types.ApplicationCommandOptionType.STRING,
            name="prefix",
            description="The prefix to use",
            required=True,
        )
    )
    prefixes.add_option(
        types.ApplicationCommandOption(
            type=types.ApplicationCommandOptionType.STRING,
            name="suffix",
            description="The suffix to use",
            required=True,
        )
    )
    count = types.ApplicationCommandOption(
        type=types.ApplicationCommandOptionType.INTEGER,
        name="number",
        description="The number of names to generate",
        required=False,
        min_value=1,
        max_value=10,
    )
    suffixes.add_option(count)
    prefixes.add_option(count)


@discord.command(description="Generate names")
def names(interaction: interactions.ChatInteraction) -> types.InteractionResponse:
    if options := interaction.data.options:
        value = int(options[0].value)  # type: ignore
    else:
        value = 10

    names = random_names(value)
    return content_response("\n".join(names))

arg = types.ApplicationCommandOption(
    type=types.ApplicationCommandOptionType.INTEGER,
    name="number",
    description="The number of names to generate",
    required=False,
    min_value=1,
    max_value=10,
)
names.add_option(arg)
