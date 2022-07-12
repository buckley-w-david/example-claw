import random
from typing import Optional, List, cast

from flask_discord_interactions import Discord
from flask_discord_interactions import discord_types as types

import importlib.resources as pkg_resources

import example_claw

prefix_corpus = [
    line for l in pkg_resources.read_text(example_claw, "prefix.txt").split("\n") if (line := l.strip().lower())
]
suffix_corpus = [
    line for l in pkg_resources.read_text(example_claw, "suffix.txt").split("\n") if (line := l.strip().lower())
]

discord = Discord()


def random_name(*, prefix: Optional[str] = None, suffix: Optional[str] = None) -> str:
    if not prefix:
        prefix = random.choice(prefix_corpus)
    if not suffix:
        suffix = random.choice(suffix_corpus)
    return f"{prefix.capitalize()}{suffix.lower()}"


with discord.command("generate") as command:
    command.description = "Special name generation"

    @command.subcommand("suffixes")
    def suffixes(interaction: types.ChatInteraction) -> types.InteractionResponse:
        options = cast(List, interaction.data.options)[0].options
        prefix = options[0].value
        if len(options) > 1:
            value = int(options[1].value)
        else:
            value = 10

        names = [random_name(prefix=prefix) for _ in range(value)]

        return types.InteractionResponse(
            type=types.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            data=types.InteractionCallbackDataMessages(
                content="\n".join(names),
            ),
        )

    suffixes.description = "Generate suffixes to go with a chosen prefix."

    @command.subcommand("prefixes")
    def prefixes(interaction: types.ChatInteraction) -> types.InteractionResponse:
        options = cast(List, interaction.data.options)[0].options
        suffix = options[0].value
        if len(options) > 1:
            value = int(options[1].value)
        else:
            value = 10

        names = [random_name(suffix=suffix) for _ in range(value)]

        return types.InteractionResponse(
            type=types.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            data=types.InteractionCallbackDataMessages(
                content="\n".join(names),
            ),
        )

    prefixes.description = "Generate prefixes to go with a chosen suffix."

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


@discord.command()
def names(interaction: types.ChatInteraction) -> types.InteractionResponse:
    if options := interaction.data.options:
        value = int(options[0].value)  # type: ignore
    else:
        value = 10

    names = [random_name() for _ in range(value)]

    return types.InteractionResponse(
        type=types.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=types.InteractionCallbackDataMessages(
            content="\n".join(names),
        ),
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
