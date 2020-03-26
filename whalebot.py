import discord

from discord.ext import commands
from discord.utils import get

from command import Command

from random import shuffle
from enum import Enum, auto

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

prefix = ">>"

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
    
    # Prints the details of the message
    print(message.channel.name + " -> " + message.author.name + ": " + message.content + "\n")

    # Processes any other commands
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


@client.command()
async def tester(ctx, *, post=""):

    if running_game:
        print("wtf")

    args = post.split()

    print(type(args))
    print(len(args))
    print(args)

# ----------------------------------------------------------------------- #

""" Testing Functions """

# Prints out a list of members in your channel
@client.command()
async def channel_members(ctx, *, post=""):
    args = post.split()

    channel = user_channel(ctx)

    if channel:
        members = channel.members
        
        output = "Members in \"" + channel.name + "\":\n"

        for member in members:
            output += member.display_name + "\n"

        output += "\n"
        print(output)

        await ctx.send(output)




@client.command()
async def current_channel(ctx, *, post=""):
    args = post.split()
    
    # global voice

    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        print(ctx.message.author.display_name + " is in: " + channel.name)
        await ctx.send(ctx.message.author.display_name + " is in: " + channel.name)
    else:
        print(ctx.message.author.display_name + " is in not in a voice channel currently")
        await ctx.send(ctx.message.author.display_name + " is in not in a voice channel currently")


    # voice = get(bot.voice_clients, guild=ctx.guild)


# ----------------------------------------------------------------------- #

""" Helper Functions """

# Returns the voice channel from a context
def user_channel(ctx):

    user = ctx.message.author

    # Returns the voice channel if exists
    if user.voice:
        return user.voice.channel
    else:
        return None


# Returns True if a game is active
def gameactive():
    if running_game:
        return True
    return False



# The command able to be used
command_dict = {"help": Help,
                "commands": Commands,
                "game": Game
               }


# ----------------------------------------------------------------------- #

""" Game Functions """

# The game that is currently being played
running_game = None

@client.command()
async def game(ctx, *, post=""):
    args = post.split()


    # Checks if a game is actives
    if gameactive():
        await ctx.send("`There is already a game running on this server\nOnly one game can be played at a time currently`")
        return

    if len(args) == 0:
        await ctx.send("`You need to pick a game to play`")
        return

    elif len(args) != 1:
        return

    if args[0] in games_dict or True:
        
        member = ctx.message.author
        running_game = games_dict.get(args[0])(member)

        await running_game.setup_game()

        
# Discord function to check if a game is active
@client.command()
async def activegame(ctx, *, post=""):
    args = post.split()

    if gameactive():
        await ctx.send(running_game.game_name)
    else:
        await ctx.send("There is no game running")


# ----------------------------------------------------------------------- #

""" Game Template """

class Game():
    
    def __init__(self, head_player):

        # Determines whether the game has been setup or not
        self.game_setup = GameSetup.PlayerAdding

        # The player who will setup the game and the characters/rules
        self.head_player = head_player


games_dict = {
    "werewolf": WerewolfGame
}

# ----------------------------------------------------------------------- #

""" Werewolf Game """

class TeamAlign(Enum):
    """Player Role team attributes"""
    Werewolf = auto()
    Villager = auto()


class TeamAppearance(Enum):
    """Player Role team appearance, this may be different to TeamAlign for roles such as lycan"""
    Werewolf = auto()
    Villager = auto()

class GameSetup(Enum):
    PlayerAdding = auto()
    RoleSelection = auto()
    Setup = auto()
    Complete = auto()


class WerewolfGame(Game):
    """The class for the game engine."""

    game_name = "Werewolf"

    # SETUP

    def __init__(self, head_player):
        super(self, head_player)
        """Takes a list of tuples for players, the tuples will be (player_id, player_name)"""

        

        # lists of player objects, either alive or dead

        self.players_alive = []
        self.players_dead = []

        # list of roles in play, with each role occurring as many times as players with that role
        # List of string role names
        self.role_list = []

        # Whether the game is still in setup phase, which allows for adding/removing players, etc.
        self.in_setup = True

    async def setup_game(self):
        
        if self.game_setup == GameSetup.PlayerAdding:
            await self.head_player.send("How many playerse are playing?")
            await self.head_player.send("Yoyo piraka")
 


    def add_player(self, user):
        """Instantiates a new player to the game, and adds them to the game's.players_alive list.
        Takes a discord user object."""

        if self.in_setup:
            self.players_alive.append(Player(user, self))
            print(user.name, user.id, "was added to the game")

    def remove_player(self, player_id):
        """Removes a player from the game.
         Takes a player_id int."""

        if self.in_setup:
            player = self.find_players(player_id)
            self.players_alive.remove(player)
            print(player.user.name, player.user.id, "was removed from the game")

    def add_role(self, role_name):
        """Adds a role_name to the role_list"""

        if self.in_setup:
            self.role_list.append(role_name)
            print(self.role_list)

    def remove_role(self, role_name):
        """Removes a role_name from the role_list"""

        if self.in_setup:
            self.role_list.remove(role_name)
            print(self.role_list)

    def assign_roles(self):
        """Shuffle the role_list and assign each player a random role.
        # Also adds each player to the game's.roles_players dict and games's.teams_players dict.
        Only call once all players have been added. Ends setup phase."""

        if self.in_setup:
            shuffled_role_list = self.role_list
            shuffle(shuffled_role_list)

            for player in self.players_alive:
                role_name = shuffled_role_list.pop()

                player.assign_role(role_name, self)

            # Ends the setup phase
            self.in_setup = False

    # GAMEPLAY

    def find_players(self, user_id=None, role=None, team=None):
        """Takes a user_id int, returns the relevant player object from the players_alive list.
        Alternatively takes a role (string role.name) and/or TeamAlign (eg. TeamAlign.Villager)
        and returns a list of all the player objects which meet the criteria.
        In the case no identifiers are specified, or no live players meet the criteria, returns an empty list."""

        players_found = []

        for player in self.players_alive:
            if user_id:
                # For finding a single alive player
                if player.user.id == user_id:
                    return player

            # For finding a list of players alive
            if role:
                if player.role.name == role:
                    players_found.append(player)
            if team:
                if player.role.team == team:
                    players_found.append(player)

        return players_found

    def game_over(self):
        """Checks whether any team has won"""

        teams_alive = set()
        for player in self.players_alive:
            teams_alive.add(player.role.team)

        if len(teams_alive) > 1:
            return False
        else:
            return True  # Could make it return the team that has won

    def kill(self, player):
        """Kills a player, moving them from the alive list to the dead list"""

        self.players_dead.append(player)

        self.players_alive.remove(player)

        player.kill()


class Player:
    """For each player in the game, defined by discord user object.
    Each player will have a role attribute"""

    def __init__(self, user, game):
        
        # Discord User
        self.user = user
        # user.id, user.name, user.dm_channel

        # The game instance this player is a part of
        self.game = game

        # The player's game attributes

        self.alive = True
        self.role = None

    def assign_role(self, role_name, game):
        """Updates the player's role, to an instance of the relevant role object"""

        # A dictionary of roles that are present, keys are names as strings, values are the role class objects
        available_roles = {role_class.name: role_class for role_class in Role.__subclasses__()}

        self.role = available_roles[role_name](game)

    def kill(self):
        """Kills the player.
        Called by the game's kill function"""

        # executes any events that occur when that role is killed
        self.role.kill()

        self.alive = False

        print(self.user.name, "has been killed, they were on ", self.role.team)


class Role:

    # Attributes that will be the same for each of that role
    name = None
    team = None
    team_appearance = None

    # Value of the player for game balancing
    player_worth = None

    # Precedence player will be called at the night phase
    night_rank = 0

    def __init__(self, game):

        # The game instance this role is a part of, allows for calling WerewolfGame methods, eg. for win_condition
        self.game = game
    
    """Some roles may have attributes modifiable for different rulesets,
    eg. bodyguard, can be able to protect self/not, can protect same person twice/not"""

    # Any special cases that happen on the first night
    def first_night(self):
        pass

    # If player has no night action function will do nothing
    def night_action(self):
        pass

    def kill(self):
        pass


class Villager(Role):
    """The villager role"""

    name = "Villager"
    team = TeamAlign.Villager
    team_appearance = TeamAppearance.Villager

    player_worth = 1


class Werewolf(Role):
    """The werewolf role"""

    name = "Werewolf"
    team = TeamAlign.Werewolf
    team_appearance = TeamAppearance.Werewolf

    def night_action(self):
        
        # Killing player

        pass


class Seer(Role):
    """The seer role"""

    name = "Seer"
    team = TeamAlign.Villager
    team_appearance = TeamAppearance.Villager

    def night_action(self):
        return super().night_action()


if __name__ == "__main__":
    """Just for some testing and debugging. Sets up a game with players and assigns roles.
    Can kill players with player.kill(), can view players' statuses with game_state(),
    and can test investigate specific players with find_players(...)"""

    class DummyUser:
        """A dummy user class to emulate the discord API user object.
        Attributes: id (int), name (string)"""
        def __init__(self, id, name):
            self.id = id
            self.name = name

    def game_state(game):
        if not game.in_setup:
            print("id name     role      team               alive")
            for player in game.players_alive + game.players_dead:
                print('{:2} {:8} {:9} {:13} {!s:5}'.format(player.user.id, player.user.name, player.role.name,
                                                           player.role.team, player.alive))

        else:
            print("SETUP", "id name")
            for player in game.players_alive + game.players_dead:
                print('{:2} {:8}'.format(player.user.id, player.user.name,))

    w_game = WerewolfGame()

    test_user_list = [DummyUser(1, 'Raph'), DummyUser(2, 'Martin'), DummyUser(3, 'Louis'), DummyUser(4, 'Tom')]
    test_role_list = ['Villager', 'Villager', 'Seer', 'Werewolf']

    for user in test_user_list:
        w_game.add_player(user)
    for role_name in test_role_list:
        w_game.add_role(role_name)

    # game_state(w_game)

    w_game.assign_roles()

    print('')
    game_state(w_game)



# ----------------------------------------------------------------------- #



if __name__ == "__main__":
    
    client.run(token)
    