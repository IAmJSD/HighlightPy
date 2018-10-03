from core import client, Cog
from discord.ext import commands
import discord
import time

version = "1.00a1"
# TODO: Adjust version as needed.


class Information(Cog):
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

    @commands.command(aliases=["details", "what", "isthisgab"])
    async def info(self, ctx):
        """Tells you some information about me!"""
        embed = discord.Embed(
            color=0x3669FA,
            title=f"Hi, I'm {client.user}",
            description=f"I'm running `HighlightPy` v**{version}**!\n"
            "My source code is available [here](https://github.com/"
            "JakeMakesStuff/HighlightPy)!\nTo learn more about using me, "
            "run `h!help`!"
        )
        embed.set_thumbnail(url=client.user.avatar_url)
        await ctx.channel.send(embed=embed)

    @staticmethod
    async def can_it_run(cmd, ctx):
        """Checks if a command can run and returns a string."""
        try:
            return "Can run" if (await cmd.can_run(ctx)) else "Can't run"
        except (commands.CheckFailure, commands.CommandError):
            return "Can't run"

    async def show_one_command(self, cmd, ctx):
        """Shows help about one specific command."""
        can_run = await self.can_it_run(cmd, ctx)
        title = f"h!{cmd.name} "
        if cmd.usage and cmd.usage != "":
            title += f"{cmd.usage} "
        title += f"({can_run})"
        description = f"{cmd.help}"
        embed = discord.Embed(
            color=0x3669FA,
            title=title,
            description=description
        )
        embed.set_thumbnail(url=client.user.avatar_url)
        await ctx.channel.send(embed=embed)

    @staticmethod
    async def render_help_page(msg, page, add_buttons=False):
        """Renders the current help page."""
        try:
            cog = client.cog_list[page - 1]
        except IndexError:
            page = len(client.cog_list)
            cog = client.cog_list[page - 1]

        cog_cmds = cog.commands
        cog_string = ""

        for cmd in cog_cmds:
            text = f"- h!{cmd.name} "
            if cmd.usage and cmd.usage != "":
                text += f"{cmd.usage} "
            text += f"- {cmd.help}\n"
            cog_string += text

        author_id = msg.embeds[0].footer.text.split(" ")[0]

        embed = discord.Embed(
            color=0x3669FA,
            title=f"{cog.name} Commands:",
            description=cog_string
        )
        embed.set_footer(
            text=f"{author_id} - Page {page}/{len(client.cog_list)}"
        )

        await msg.edit(embed=embed)

        if add_buttons:
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")

    async def show_default_help(self, ctx):
        """Shows the default help command."""
        embed = discord.Embed(
            title="Loading..."
        )
        embed.set_footer(text=f"{ctx.author.id}")
        msg = await ctx.channel.send(embed=embed)
        await self.render_help_page(msg, 1, True)

    @commands.command(usage="[command]")
    async def help(self, ctx, *, command_name: str=None):
        """Gets help about the bot/a specific command."""
        if command_name:
            cmd = ctx.bot.get_command(command_name)
            if not cmd:
                embed = discord.Embed(
                    color=discord.Colour.red(),
                    title="I couldn't find that command.",
                    description="Use `h!help` to see a list of commands."
                )
                embed.set_thumbnail(url=client.user.avatar_url)
                return await ctx.channel.send(embed=embed)
            return await self.show_one_command(cmd, ctx)

        return await self.show_default_help(ctx)

    async def on_reaction_add(self, reaction, user):
        """Handles reaction page switch-eroos."""
        if reaction.message.author.id != client.user.id:
            return

        if len(reaction.message.embeds) == 0:
            return

        embed = reaction.message.embeds[0]

        if not embed.footer or not embed.footer.text:
            return

        footer_text_split = embed.footer.text.split(" ")

        try:
            if footer_text_split[2] != "Page":
                return
        except IndexError:
            return

        page = int(footer_text_split[3].split("/")[0])
        author = int(footer_text_split[0])

        if user.id != author:
            return

        max_pages = len(client.cog_list)

        try:
            await reaction.message.remove_reaction(reaction.emoji, user)
        except discord.Forbidden:
            pass

        if str(reaction.emoji) == "◀":
            new_page = page - 1
        elif str(reaction.emoji) == "▶":
            new_page = page + 1
        else:
            return

        if new_page == 0 or new_page > max_pages:
            return

        await self.render_help_page(reaction.message, new_page)


client.add_cog(Information())
# Adds the cog.
