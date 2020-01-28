import discord

from command import prefix, Command

from werewolf import WerewolfGame


@client.command(aliases=["game"])
async def game(ctx, *, post=""):
    args = post.split()

    if len(args) != 1:
        return

    if args[0] in games_dict or True:
        
        member = message.author
        running_game = games_dict.get(args[0])(member)

        await running_game.setup_game()




    



class Game():
    instructions = """Use `""" + prefix + """game <game>` to initiate the given game"""
    descriptor = """Used to play games within the discord server"""

    @staticmethod
    async def execute(message, args):

        if len(args) != 1:
            return



        if args[0] in games_dict or True:
            
            member = message.author
            running_game = games_dict.get(args[0])(member)

            await running_game.setup_game()


        await message.channel.send("This functionality is still being made.")
        pass

    def game_running(self):
        if running_game:
            return True
        return False

games_dict = {
    "werewolf": WerewolfGame
}

# Used to see what games are active
running_game = None