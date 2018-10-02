from core import client
from discord.ext import commands
import discord
import time


class Information:
    """Commands which show information about the bot."""
    @commands.command()
    async def ping(self, ctx):
        """Pings the bot."""
        start = time.perf_counter()
        message = await ctx.channel.send('Ping...')
        end = time.perf_counter()
        duration = (end - start) * 1000

        await message.edit(
            content='**Command Ping:** {:.2f}ms\n**WS Ping:** {:.2f}ms'.format(
                duration, ctx.bot.latency * 1000
            )
        )

    @commands.command()
    async def invite(self, ctx):
        """Gives a invite for the bot."""
        embed = discord.Embed(
            color=0x3669FA,
            title=f"Thanks for choosing {client.user.name}!",
            description="To invite me to your server, please use [this]"
            "(https://discordapp.com/oauth2/authorize?client_id="
            f"{client.user.id}&scope=bot&permissions=84992) link!"
        )
        embed.set_thumbnail(url=client.user.avatar_url)
        await ctx.channel.send(embed=embed)


client.add_cog(Information())
# Adds the cog.
