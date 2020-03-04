import discord

from discord.ext import commands

from command import prefix, Command
from games import Game, running_game


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = commands.Bot(command_prefix = prefix)
client.remove_command('help')
# client = discord.Client()

# Anything that is done at on bot startup
@client.event
async def on_ready():
    
    await client.change_presence(activity=discord.Game(name=prefix + 'help for info'))
    print("Whalebot is now live!\n")

@client.event
async def on_message(message):
    
    # A command has been initiated
    # if message.content.startswith(prefix):
    #     line_split = message.content[2:].split()
    #     command = line_split[0]
    #     args = line_split[1:]

    #     print("command: " + command + "\nargs: " + str(args))

    #     if command in command_dict.keys():
    #         await command_dict.get(command).execute(message, args)

    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    pass

class Help(Command):

    instructions = """Type `""" + prefix + """help <command>` to figure out what other commands do"""
    descriptor = """Gives help with how to use the bot and how commands work"""

    @staticmethod
    async def execute(message, args):
        if len(args) == 0:
            await message.channel.send("""Type: `>> + <command>` to use our commands, full list of commands in `>>commands`""")
        elif len(args) == 1:
            if args[0] in command_dict.keys():
                await message.channel.send(command_dict.get(args[0]).instructions)

class Commands(Command):

    instructions = """Simply use `""" + prefix + """commands` to bring up a list of commands and their descriptions"""
    descriptor = """Lists the commands the bot can use"""

    @staticmethod
    async def execute(message, args):
        reply = "Commands:"

        for name, instance in sorted(command_dict.items()):
            line = "\n`" + prefix + name + "`" + " - " + instance.descriptor
            print(line)
            reply = reply + line

        print(reply)
        await message.channel.send(reply)



# Commands
@client.command()
async def help(ctx, *, post=""):

    args = post.split()


    if len(args) == 0:
        await ctx.send("""Type: `"""+ prefix + """ + <command>` to use our commands, full list of commands in `""" + prefix + """commands`""")
    elif len(args) == 1:
        if args[0] in command_dict.keys():
            await ctx.send(command_dict.get(args[0]).instructions)


@client.command()
async def commands(ctx, *, post=""):

    args = post.split()

    reply = "Commands:"

    for name, instance in sorted(command_dict.items()):
        line = "\n`" + prefix + name + "`" + " - " + instance.descriptor
        print(line)
        reply = reply + line

    print(reply)
    await ctx.send(reply)


@client.command(aliases=["dindu"])
async def tester(ctx, *, post=""):

    poast = args.split()
    print(type(args))
    print(len(args))
    print(args)


@client.command()
async def game(ctx, *, post=""):
    args = post.split()

    if len(args) == 0:
        await ctx.send("You need to pick a game to play")
        return

    elif len(args) != 1:
        return

    if args[0] in games_dict or True:
        
        member = message.author
        running_game = games_dict.get(args[0])(member)

        await running_game.setup_game()

# The command able to be used
command_dict = {"help": Help,
                "commands": Commands,
                "game": Game
               }



if __name__ == "__main__":
    
    client.run(token)
    