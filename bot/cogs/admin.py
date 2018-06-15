from bot.constants import ADMIN_ROLES, BANNED_DOMAINS

from discord import Member
from discord.ext.commands import Bot, Context, command, has_any_role


class Admin:
    """
    Administration related commands.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def mute_member(self, member: Member, reason: str="N/A"):
        self.bot.muted.append(member.id)
        print(f"Member {member} ({member.id}) has been muted: {reason}")

    @command()
    @has_any_role(*ADMIN_ROLES)
    async def mute(self, ctx: Context, member: Member):
        if any(role_name in [role.name for role in member.roles] for role_name in ADMIN_ROLES):
            await ctx.send(f"{ctx.author.mention} | Can't mute an admin!")
        else:
            self.bot.muted.append(member.id)
            await ctx.send(f"{ctx.author.mention} | {member.mention} has been muted.")
    
    @command()
    @has_any_role(*ADMIN_ROLES)
    async def unmute(self, ctx: Context, member: Member):
        self.bot.muted.remove(member.id)
        await ctx.send(f"{ctx.author.mention} | {member.mention} has been unmuted.")

    async def on_message(self, message):
        # Check if author is muted
        if message.author.id in self.bot.muted:
            await message.delete()
            await message.author.send("You are muted!")
        
        # Check if message contains a banned domain
        elif any(domain in message.content.lower() for domain in BANNED_DOMAINS):
            await message.delete()
            await message.channel.send(f"{message.author.mention} | That domain is banned! You have been muted.")
            await self.mute_member(message.author, "Message contains banned domain")

def setup(bot):
    bot.add_cog(Admin(bot))
