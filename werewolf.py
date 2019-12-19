from random import shuffle
import discord
# from collections import defaultdict

from enum import Enum, auto


class TeamAlign(Enum):
    Werewolf = auto()
    Villager = auto()


class TeamAppearance(Enum):
    Werewolf = auto()
    Villager = auto()

class GameSetup(Enum):
    PlayerAdding = auto()
    RoleSelection = auto()
    Setup = auto()
    Complete = auto()


class WerewolfGame:
    """The class for the game engine."""

    # SETUP

    def __init__(self, head_player):
        """Takes a list of tuples for players, the tuples will be (player_id, player_name)"""

        # Determines whether the game has been setup or not
        self.game_setup = GameSetup.PlayerAdding

        # The player who will setup the game and the characters/rules
        self.head_player = head_player

        # a dictionary of player objects, with their player_id as the keys
        # self.players = {}
        self.players_alive = []
        self.players_dead = []

        # list of roles in play, with each role occurring as many times as players with that role
        self.role_list = []

        # # a dictionary of players grouped by their roles, with the role name strings as keys,
        # # and a list of player objects as values
        # self.roles_players = defaultdict(list)
        # self.teams_players = defaultdict(list)

        # Whether the game is still in setup phase, which allows for adding/removing players, etc.
        self.in_setup = True

    async def setup_game(self):
        
        if self.game_setup == GameSetup.PlayerAdding:
            await self.head_player.send("How many playerse are playing?")
            await self.head_player.send("Yoyo piraka")
 


    def add_player(self, user):
        """Instantiates a new player to the game, and adds them to the game's.players_alive list"""

        if self.in_setup:
            self.players_alive.append(Player(user, self))

    def remove_player(self, player_id):
        """Removes a player from the game."""

        if self.in_setup:
            pass

    def add_role(self, role):
        """Adds a role to the role_list"""

        if self.in_setup:
            pass

    def remove_role(self, role):
        """Removes a role from the role_list"""

        if self.in_setup:
            pass

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

                # self.roles_players[role_name].append(player)
                # self.teams_players[player.role.team].append(player)

            # Ends the setup phase
            self.in_setup = False

    # GAMEPLAY

    def find_player(self, user_id):
        """Takes a user_id, returns the relevant player object from the players_alive list"""

        for player in self.players_alive:
            if player.user.id == user_id:
                return player
        
        print("Player not found.")
        return None

    # def number_alive(self, role_name=None, team_name=None, custom_player_list=None):
    #     """Returns an int, the number of remaining players of those specified that are still alive.
    #     The players under consideration can be chosen by role_name (str), team_name (str),
    #     or a custom_player_list (list).
    #     If run without arguments number_alive() returns the total number of players alive"""
    #
    #     # Finds sets of players that meet each criteria, and counts the number of those that are in all sets
    #     # that are alive
    #
    #     players = set(self.players.values())
    #
    #     if role_name:
    #         players &= set(self.roles_players[role_name])
    #
    #     if team_name:
    #         players &= set(self.teams_players[team_name])
    #
    #     if custom_player_list:
    #         players &= set(custom_player_list)
    #
    #     n = 0
    #     for player in players:
    #         n += player.alive
    #
    #     return n

    def game_over(self):
        """Checks whether any team has won"""

        teams_alive = set()
        for player in self.players_alive:
            teams_alive.add(player.role.TeamAlign)

        if len(teams_alive) > 1:
            return False
        else:
            return True

    def kill(self, player):
        """Kills a player, moving them from the alive list to the dead list"""

        self.players_dead.append(player)

        self.players_alive.pop(player)

        player.kill()


class Player:
    """For each player in the game, defined by discord user object.
    Each player will have a role attribute"""

    def __init__(self, user, game):
        
        # Discord User
        self.user = user
        # user.id, user.name

        # The game instance this player is a part of
        self.game = game

        self.alive = True
        self.role = None

    def assign_role(self, role_name, game):
        """Updates the player's role, to an instance of the relevant role object"""

        # A dictionary of roles that are present, keys are names as strings, values are the role class objects
        available_roles = {role_class.__name__: role_class for role_class in Role.__subclasses__()}

        self.role = available_roles[role_name](game)

    def kill(self):
        """Kills the player.
        Called by the game's kill function"""

        self.role.kill()

        self.alive = False

        print(self.user.name, "has been killed, they were on the", self.role.team)


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


# if __name__ == "__main__":
#     """Just for some testing and debugging. Sets up a game with players and assigns roles.
#     Can kill players with player.kill(), can view players' statuses with game_state(),
#     and can test numbers of different groups of players still alive with game.number_alive(...)"""
#     w_game = WerewolfGame([('#1', 'Raph'), ('#2', 'Martin'), ('#3', 'Louis'), ('#4', 'Tom')])
#     w_game.role_list = ['Villager', 'Villager', 'Seer', 'Werewolf']  # because not yet implemented in ruleset
#     w_game.assign_roles()
#
#     def game_state(game):
#         print("id name     role.name role.team     alive")
#         for player in game.players.values():
#             print('{:2} {:8} {:9} {:13} {!s:5}'.format(player.id, player.name, player.role.name, player.role.team,
#                                                        player.alive))
#
#     game_state(w_game)
