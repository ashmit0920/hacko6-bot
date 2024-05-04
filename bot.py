import interactions
from interactions import slash_command, SlashContext, OptionType, SlashCommandChoice, slash_option, UserConverter, Member, BaseUser, Webhook, Role, RoleConverter
from interactions import Button, ButtonStyle, ActionRow, ComponentContext, component_callback, BaseContext, StringSelectMenu, StringSelectOption
from interactions.api.events import MemberAdd, Component
import asyncio
import os
from dotenv import load_dotenv
import json

with open('teams.json', 'r') as f:
    teams = json.load(f)

INTENTS = interactions.Intents.new(
    guilds=True,
    guild_emojis_and_stickers=True,
    guild_presences=True,
    guild_members=True,
    guild_moderation=True,
    guild_messages=True,
    direct_messages=True,
    message_content=True,
)

load_dotenv(dotenv_path='D:/Hacko 6 Bot/token.env')
token = os.getenv('TOKEN')
bot = interactions.Client(intents=INTENTS)

@interactions.listen()
async def on_startup():
    print("Bot is ready!")

# Create team role
@slash_command(name="create", description="Create your team's role for HackOwasp 6.0")
async def create(ctx: SlashContext):
    pass

@create.subcommand("team", sub_cmd_description="Create your team's role for HackOwasp 6.0")
@slash_option(name="name", description="Your team's name.", opt_type=OptionType.STRING, required=True)
@slash_option(name="member1", description="Discord ID of member 1.", opt_type=OptionType.USER, required=True)
@slash_option(name="member2", description="Discord ID of member 2.", opt_type=OptionType.USER, required=True)
@slash_option(name="member3", description="Discord ID of member 3.", opt_type=OptionType.USER, required=False)
@slash_option(name="member4", description="Discord ID of member 4.", opt_type=OptionType.USER, required=False)
@slash_option(name="member5", description="Discord ID of member 5.", opt_type=OptionType.USER, required=False)

async def create_role(ctx: SlashContext, name: str, member1: Member, member2: Member, member3: Member = False, member4: Member = False, member5: Member = False, reason=None):
    guild = bot.get_guild(ctx.guild_id)

    if ctx.channel_id == 1229470228623261777 or 1: # Team creation channel
        new_role = await guild.create_role(name=name, color=interactions.RoleColors.BLUE)
        hacko_role = 1227726112453562441 # Role id of Hacko 6 role
        members = [member1.global_name, member2.global_name]
        
        await ctx.defer()
        await asyncio.sleep(5)
        
        overwrites = [
            interactions.PermissionOverwrite(id=739806361210322984, type='role', allow=0, deny=1024),  # Deny permissions to @everyone
            interactions.PermissionOverwrite(id=bot.user.id, type='member', allow=1024, deny=0),  # Allow permissions to the bot
            interactions.PermissionOverwrite(id=1022114019097710632, type='role', allow=1024, deny=0) # mod role
        ]
        team_channel = await guild.create_text_channel(name=f'{name}-text', permission_overwrites=overwrites)
        voice_channel = await guild.create_voice_channel(name=f'{name}-voice', permission_overwrites=overwrites)
        await team_channel.set_permission(new_role, view_channel=True, send_messages=True)
        await voice_channel.set_permission(new_role, view_channel=True, connect=True, speak=True)
        
        await ctx.author.add_roles([new_role, hacko_role])
        await member1.add_roles([new_role, hacko_role])
        await member2.add_roles([new_role, hacko_role])
        if member3:
            await member3.add_roles([new_role, hacko_role])
            members.append(member3.global_name)
        if member4:
            await member4.add_roles([new_role, hacko_role])
            members.append(member4.global_name)
        if member5:
            await member5.add_roles([new_role, hacko_role])
            members.append(member5.global_name)

        teams[name] = members
        
        with open("teams.json", "w") as f:
            json.dump(teams, f, indent=4)
        
        await team_channel.send(f'{new_role.mention} Welcome to HackOwasp 6.0! This is the official text channel for your team. A voice channel has also been created with the same name.')

        nl = '\n'
        embed = interactions.Embed(
            title='Role created successfully! <a:pepesaber:1167192243682148472>',
            description=f'Thank you for being a part of HackOwasp 6.0. {nl}{nl}**Your team members are:** {nl}{nl.join(members)}',
            color="#ADD8E6",
            thumbnail=bot.user.avatar.url,
        )

        await ctx.send(ctx.author.mention, embed=embed, ephemeral=True)
    
    else:
        await ctx.send("Wrong channel! Please use the command in <#1229470228623261777> only.", ephemeral=True)

# Delete team roles
@slash_command(name="delete", description="Delete all teams of HackOwasp 6.0")
async def delete(ctx: SlashContext):
    pass

@delete.subcommand("teams", sub_cmd_description="Delete all teams of HackOwasp 6.0")
async def delete_teams(ctx: SlashContext, reason=None):
    try:
        guild = bot.get_guild(ctx.guild_id)
        if ctx.author_id == 739509406798184469:
            for role in guild.roles:
                if role.name in teams.keys():
                    await role.delete()
                    await ctx.send(f'Team {role.name} has been deleted.')

        else:
            embed = interactions.Embed(
                title="Permission Denied! <a:pepemarch:1201261350287061033>",
                description=f'Only <@!739509406798184469> can run this command.',
                color="#ADD8E6",
                thumbnail=bot.user.avatar.url,
            )
            await ctx.send(embed=embed, ephemeral=True)

    except:
        embed = interactions.Embed(
                title="Unexpected error! <a:pepemarch:1228318597345050684>",
                description=f'There has been an error processing the command. Please contact <@!739509406798184469> for assistance, we regret the inconvenience caused.',
                color="#ADD8E6",
        )
        await ctx.send(embed=embed)


# Help command
@slash_command(name="help", description="Get info about the bot's commands and functionalities.")
async def help(ctx: SlashContext):
    nl = '\n'
    emoji = '<a:bluestar:1229551762688446575>'
    embed = interactions.Embed(
        title="Help Menu",
        description=f'{emoji} **/create team -** Creates a role for your team and assigns it to all the team members. The HackOwasp 6.0 role will also be assigned automatically to all the members. {nl}**Note -** The command must only be used once by any member of a team. The person using the command must select himself as a member too in the member options. {nl}{nl}{emoji} **/faq -** See a list of frequency asked questions regarding HackOwasp 6.0.',
        color="#ADD8E6",
        thumbnail=bot.user.avatar.url,
    )
    await ctx.send(embed=embed, ephemeral=True)


# FAQ command
@slash_command(name="faq", description="See a list of frequently asked questions regarding HackOwasp 6.0.")
async def faq(ctx: SlashContext):
    nl = '\n'
    emoji = '<a:bluestar:1229551762688446575>'
    embed = interactions.Embed(
        title="Frequently Asked Questions",
        description=f'{emoji} **What are the dates for HackOwasp 6.0?** {nl}The hackathon will be conducted on 19, 20 and 21 April, 2024.{nl}{nl}{emoji} **Will the hackathon be conducted online or offline?** {nl}HackOwasp 6.0 is a hybrid hackathon, with offline mode available for select TIET students only. {nl}{nl}{emoji} **How do I register for HackOwasp 6.0?** {nl}Register for the hackathon on DevFolio - https://hackowasp6.devfolio.co {nl}{nl}{emoji} **What are the prizes for the winning teams?** {nl}TBD {nl}{nl}{emoji} **Is there food provided during the Hackathon?** {nl}Yes! Dinner, late night snacks and beverages are on us ;). {nl}{nl}{emoji} **What should I bring to the Hackathon?** {nl}Laptops, chargers, extensions and some snacks are recommended. You must also bring any specific hardware relevant to your project (in case you opt for hardware tracks).',
        color="#ADD8E6",
        thumbnail=bot.user.avatar.url,
    )
    await ctx.send(embed=embed, ephemeral=True)

# Delete channels
# @slash_command(name="chdelete", description="Delete old channels.")
# async def delete(ctx: SlashContext):
#     await ctx.defer()
#     await asyncio.sleep(7)
#     guild = bot.get_guild(ctx.guild_id)
#     for ch in guild.channels:
#         if "voice" in ch.name:
#             await ch.delete()
            
#     await ctx.send("successful")

bot.start(token)
