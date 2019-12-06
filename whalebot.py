import discord


# The prefix used to call the bot
prefix = ">>"

def read_token():
    with open("./app/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()

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

class Command:

    instructions = """ """
    description = """ """

    @staticmethod
    async def execute(message, args):
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


# The command able to be used
command_dict = {"help": Help,
                "commands": Commands
               }


running_games = []


if __name__ == "__main__":
    print("Whalebot is now live!\n")
    client.run(token)