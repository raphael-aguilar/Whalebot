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

        await command_dict.get(command, help_me)(message, args)


async def help_me(message, args=None):
    await message.channel.send("""Type: `>> + <command>` to use our commands, full list of commands in `>>commands`""")
    
async def commands(message, args=None):
    reply = "Commands:"

    for i in sorted(command_dict.keys()):
        line = "\n`" + prefix + i + "`"
        print(line)
        reply = reply + line


    print(reply)
    await message.channel.send(reply)

command_dict = {"help": help_me,
                "commands": commands
               }


client.run(token)