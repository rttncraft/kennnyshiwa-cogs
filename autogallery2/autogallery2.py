import asyncio
import discord
import aiohttp
import io
from io import BytesIO
from typing import Any
from datetime import datetime
from redbot.core import Config, checks, commands

from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class Autogallery2(Cog):
    """
    Auto post videos into a gallery!
    """

    __author__ = "kennnyshiwa"

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=376564057517457408, force_registration=True
        )
        default_guild = {
            "channel": None,
            "channels": [],
        }
        
        self.config.register_guild(**default_guild)


    @commands.command()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @checks.bot_has_permissions(manage_messages=True)
    async def addautogallery2(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        """Add a channel to the list of Gallery channels."""
        if channel.id not in await self.config.guild(ctx.guild).channels():
            async with self.config.guild(ctx.guild).channels() as channels:
                channels.append(channel.id)
            await ctx.send(f"{channel.mention} has been added into the Gallery channels list.")
        else:
            await ctx.send(f"{channel.mention} is already in the Gallery channels list.")

    @commands.command()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @checks.bot_has_permissions(manage_messages=True)
    async def rmautogallery2(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        """Remove a channel from the list of Gallery channels."""
        if channel.id in await self.config.guild(ctx.guild).channels():
            async with self.config.guild(ctx.guild).channels() as channels:
                channels.remove(channel.id)
            await ctx.send(f"{channel.mention} has been removed from the Gallery channels list.")
        else:
            await ctx.send(f"{channel.mention} already isn't in the Gallery channels list.")
    
    @commands.command()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @checks.bot_has_permissions(manage_messages=True)
    async def gallery2channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """Add the gallery channel for auto posting videos"""
        autochannel = await self.config.guild(ctx.guild).channel()
        if autochannel is None:
            if channel is not None:
                channelid = channel.id
            await self.config.guild(ctx.guild).channel.set(channelid)
            await ctx.send(f"{channel.mention} has been set as the gallery channel")
        else:
            await ctx.send(f"{channel.mention} is already in the Gallery channels list.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.channel.id not in await self.config.guild(message.guild).channels():
            return
        if not message.attachments:
            return
        gallery = await self.config.guild(message.guild).channel()
        if not gallery:
            return
        gallerychannel = self.bot.get_channel(gallery)
        for attachment in message.attachments:
            if attachment.filename.endswith(".mp4") or attachment.filename.endswith(".mov") or attachment.filename.endswith(".avi"):
                pass
            else:
                return
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status != 200:
                        return
                    data = await resp.read()
            await gallerychannel.send(file=discord.File(io.BytesIO(data), filename=attachment.filename))

