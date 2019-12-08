import discord

from command import prefix, Command

class Game():
    instructions = """Use `""" + prefix + """game <game>` to initiate the given game"""
    descriptor = """Used to play games within the discord server"""

    @staticmethod
    async def execute(message, args):
        await message.channel.send("This functionality is still being made.")
        pass


games_dict = {

}

# Used to see what games are active
running_games = []