import discord

from command import prefix, Command
from games import Game, running_game


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()


async def set_status():
    activity = discord.Activity(name='hello there', type=discord.Activity.watching)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    
    # A command has been initiated
    if message.content.startswith(prefix):
        line_split = message.content[2:].split()
        command = line_split[0]
        args = line_split[1:]

        print("command: " + command + "\nargs: " + str(args))

        if command in command_dict.keys():
            await command_dict.get(command).execute(message, args)

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

# The command able to be used
command_dict = {"help": Help,
                "commands": Commands,
                "game": Game
               }



if __name__ == "__main__":
    
    client.run(token)
    set_status()
    print("Whalebot is now live!\n")
    