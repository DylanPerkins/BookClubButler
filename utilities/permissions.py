from discord_http import CheckFailed, Context

import discord_http


def can_handle(ctx: "Context", permission: str) -> bool:
    """Checks if bot has permissions or is in DMs right now"""
    return isinstance(ctx.channel, discord_http.DMChannel) or getattr(
        ctx.channel.permissions_for(ctx.guild.me), permission
    )


def is_owner(ctx: Context):
    """Check if the user is the owner of the bot."""
    if str(ctx.user.id) != str(ctx.bot.config.discord_owner_id):
        raise CheckFailed("You are not the owner of the bot.")

    return True


def is_administrator(ctx: Context):
    if not ctx.user.guild_permissions.administrator:
        raise CheckFailed("You do not have administrator permissions.")

    return True


def is_capable(ctx: Context):
    """Check if the user has administrator permissions."""
    if isinstance(ctx.channel, discord_http.DMChannel):
        raise CheckFailed("This command cannot be used in DMs.")

    if not ctx.user.guild_permissions.administrator:
        raise CheckFailed("You do not have administrator permissions.")

    if str(ctx.user.id) != str(ctx.bot.config.discord_owner_id):
        raise CheckFailed("You are not the owner of the bot.")

    return True
