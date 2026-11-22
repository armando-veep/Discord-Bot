import datetime
import json
import os
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

WARNINGS_FILE = "WARNINGS_FILE_PATH.json"  # Example: "warnings.json"


def load_warnings() -> dict:
    if not os.path.exists(WARNINGS_FILE):
        return {}
    with open(WARNINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_warnings(data: dict) -> None:
    with open(WARNINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Moderation(commands.Cog):
    """COG_DESCRIPTION_PENDING"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.warnings = load_warnings()

    async def _can_moderate(
        self, ctx: commands.Context, target: discord.Member, action: str
    ) -> bool:
        """Verifies role hierarchy to prevent abuse or permission errors."""
        if target.id == ctx.author.id:
            await ctx.send(f"ERROR_SELF_MODERATION_PENDING ({action})", ephemeral=True)
            return False

        if target.id == self.bot.user.id:
            await ctx.send(f"ERROR_MODERATING_BOT_PENDING ({action})", ephemeral=True)
            return False

        if ctx.guild.owner_id != ctx.author.id:
            if target.top_role >= ctx.author.top_role:
                await ctx.send(
                    f"ERROR_USER_HIERARCHY_PENDING ({target})",
                    ephemeral=True,
                )
                return False

        if target.top_role >= ctx.guild.me.top_role:
            await ctx.send(
                f"ERROR_BOT_HIERARCHY_PENDING ({action} -> {target})",
                ephemeral=True,
            )
            return False

        return True

    def _build_embed(
        self,
        title: str,
        color: discord.Color,
        target: discord.abc.User,
        moderator: discord.abc.User,
        reason: str,
        extra: Optional[str] = None,
    ) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        embed.add_field(
            name="EMBED_FIELD_USER_PENDING",
            value=f"{target} (`{target.id}`)",
            inline=False,
        )
        embed.add_field(
            name="EMBED_FIELD_MODERATOR_PENDING",
            value=f"{moderator.mention} (`{moderator.id}`)",
            inline=False,
        )
        embed.add_field(
            name="EMBED_FIELD_REASON_PENDING",
            value=reason,
            inline=False,
        )
        if extra:
            embed.add_field(
                name="EMBED_FIELD_DETAILS_PENDING",
                value=extra,
                inline=False,
            )
        return embed

    @commands.hybrid_command(
        name="KICK_COMMAND_NAME_PENDING",
        description="KICK_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        member="MEMBER_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        if not await self._can_moderate(ctx, member, "kick"):
            return

        try:
            await member.send(f"DM_KICK_MESSAGE_PENDING ({ctx.guild.name} | {reason})")
        except discord.Forbidden:
            pass

        await member.kick(reason=f"{reason} | {ctx.author}")
        embed = self._build_embed(
            "EMBED_TITLE_KICK_PENDING",
            discord.Color.orange(),  # EMBED_COLOR_PENDING
            member,
            ctx.author,
            reason,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="BAN_COMMAND_NAME_PENDING",
        description="BAN_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        user="USER_PARAMETER_DESCRIPTION_PENDING",
        delete_days="DELETE_DAYS_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        user: discord.User,
        delete_days: app_commands.Range[int, 0, 7] = 1,
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        member = ctx.guild.get_member(user.id)
        if member and not await self._can_moderate(ctx, member, "ban"):
            return

        if member:
            try:
                await member.send(f"DM_BAN_MESSAGE_PENDING ({ctx.guild.name} | {reason})")
            except discord.Forbidden:
                pass

        await ctx.guild.ban(
            user,
            delete_message_seconds=delete_days * 86400,
            reason=f"{reason} | {ctx.author}",
        )
        embed = self._build_embed(
            "EMBED_TITLE_BAN_PENDING",
            discord.Color.red(),  # EMBED_COLOR_PENDING
            user,
            ctx.author,
            reason,
            extra=f"EXTRA_TEXT_MESSAGES_DELETED_PENDING: {delete_days}",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="UNBAN_COMMAND_NAME_PENDING",
        description="UNBAN_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        user_id="USER_ID_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        user_id: str,
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        if not user_id.isdigit():
            await ctx.send("ERROR_INVALID_ID_PENDING", ephemeral=True)
            return

        user = discord.Object(id=int(user_id))
        try:
            await ctx.guild.unban(user, reason=f"{reason} | {ctx.author}")
        except discord.NotFound:
            await ctx.send("ERROR_USER_NOT_BANNED_PENDING", ephemeral=True)
            return

        embed = self._build_embed(
            "EMBED_TITLE_UNBAN_PENDING",
            discord.Color.green(),  # EMBED_COLOR_PENDING
            user,
            ctx.author,
            reason,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="TIMEOUT_COMMAND_NAME_PENDING",
        description="TIMEOUT_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        member="MEMBER_PARAMETER_DESCRIPTION_PENDING",
        minutes="MINUTES_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        if not await self._can_moderate(ctx, member, "timeout"):
            return

        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=f"{reason} | {ctx.author}")

        embed = self._build_embed(
            "EMBED_TITLE_TIMEOUT_PENDING",
            discord.Color.gold(),  # EMBED_COLOR_PENDING
            member,
            ctx.author,
            reason,
            extra=f"EXTRA_TEXT_DURATION_PENDING: {minutes}",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="UNTIMEOUT_COMMAND_NAME_PENDING",
        description="UNTIMEOUT_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        member="MEMBER_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def untimeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        await member.timeout(None, reason=f"{reason} | {ctx.author}")
        embed = self._build_embed(
            "EMBED_TITLE_UNTIMEOUT_PENDING",
            discord.Color.blurple(),  # EMBED_COLOR_PENDING
            member,
            ctx.author,
            reason,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="PURGE_COMMAND_NAME_PENDING",
        description="PURGE_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        amount="AMOUNT_PARAMETER_DESCRIPTION_PENDING",
        member="USER_FILTER_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(
        self,
        ctx: commands.Context,
        amount: app_commands.Range[int, 1, 100],
        member: Optional[discord.Member] = None,
    ) -> None:
        if ctx.interaction:
            await ctx.defer(ephemeral=True)

        check = (lambda m: m.author.id == member.id) if member else None
        deleted = await ctx.channel.purge(limit=amount + (0 if ctx.interaction else 1), check=check)

        msg = f"PURGE_CONFIRMATION_TEXT_PENDING ({len(deleted)})"
        if member:
            msg += f" | USER_FILTER_TEXT_PENDING ({member})"

        await ctx.send(msg, ephemeral=True)

    @commands.hybrid_command(
        name="WARN_COMMAND_NAME_PENDING",
        description="WARN_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(
        member="MEMBER_PARAMETER_DESCRIPTION_PENDING",
        reason="REASON_PARAMETER_DESCRIPTION_PENDING",
    )
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = "DEFAULT_REASON_PENDING",
    ) -> None:
        if not await self._can_moderate(ctx, member, "warn"):
            return

        guild_key = str(ctx.guild.id)
        user_key = str(member.id)

        self.warnings.setdefault(guild_key, {}).setdefault(user_key, []).append(
            {
                "reason": reason,
                "moderator_id": ctx.author.id,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        )
        save_warnings(self.warnings)

        total = len(self.warnings[guild_key][user_key])
        embed = self._build_embed(
            "EMBED_TITLE_WARN_PENDING",
            discord.Color.yellow(),  # EMBED_COLOR_PENDING
            member,
            ctx.author,
            reason,
            extra=f"EXTRA_TEXT_TOTAL_WARNINGS_PENDING: {total}",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="WARNINGS_COMMAND_NAME_PENDING",
        description="WARNINGS_COMMAND_DESCRIPTION_PENDING",
    )
    @app_commands.describe(member="MEMBER_PARAMETER_DESCRIPTION_PENDING")
    @commands.has_permissions(moderate_members=True)
    async def list_warnings(self, ctx: commands.Context, member: discord.Member) -> None:
        user_warns = self.warnings.get(str(ctx.guild.id), {}).get(str(member.id), [])
        if not user_warns:
            await ctx.send(f"TEXT_NO_WARNINGS_PENDING ({member})", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"EMBED_TITLE_LIST_WARNINGS_PENDING ({member})",
            color=discord.Color.yellow(),  # EMBED_COLOR_PENDING
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        for idx, item in enumerate(user_warns[-10:], start=1):
            embed.add_field(
                name=f"WARNING_FIELD_TITLE_FORMAT_PENDING #{idx} — <@{item['moderator_id']}>",
                value=f"REASON_TEXT_PENDING: {item['reason']}\n`{item['timestamp'][:10]}`",
                inline=False,
            )
        await ctx.send(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        error = getattr(error, "original", error)

        if isinstance(error, (commands.MissingPermissions, app_commands.MissingPermissions)):
            await ctx.send("ERROR_USER_MISSING_PERMISSIONS_PENDING", ephemeral=True)
        elif isinstance(error, (commands.BotMissingPermissions, app_commands.BotMissingPermissions)):
            await ctx.send("ERROR_BOT_MISSING_PERMISSIONS_PENDING", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("ERROR_INVALID_ARGUMENT_PENDING", ephemeral=True)
        elif isinstance(error, discord.Forbidden):
            await ctx.send("ERROR_DISCORD_FORBIDDEN_PENDING", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
