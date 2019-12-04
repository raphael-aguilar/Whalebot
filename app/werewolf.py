import random
import discord
from collections import defaultdict


class WerewolfGame:
    """The class for the game engine.
    Will need to know the players (by discord ID # and name)
    And the ruleset - the roles in play, how many of each, and any modifiers"""

    # SETUP

    def __init__(self, player_list, ruleset=None):
        """Takes a list of tuples for players, the tuples will be (player_id, player_name)"""

        # a dictionary of player objects, with their player_id as the keys
        self.players = {}

        for player_id, player_name in player_list:
            self.add_player(player_id, player_name)

        # probably a dict of {'role':{modifier1:value, modifier2:value},...}, with each role in play included just once
        # most will just be empty/default, these can be the arguments for when the roles are initialised
        # created from ruleset
        # self.role_modifiers = {}

        # list of roles in play, with each role occurring as many times as players with that role
        # created from ruleset
        self.role_list = []

        # a dictionary of players grouped by their roles, with the role name strings as keys,
        # and a list of player objects as values
        self.roles_players = defaultdict(list)
        self.teams_players = defaultdict(list)

    def add_player(self, player_id, player_name):
        """Instantiates a new player to the game, and adds them to the game's.players dictionary"""

        self.players[player_id] = Player(player_id, player_name)

    def assign_roles(self):
        """Shuffle the role_list and assign each player a random role.
        Also adds each player to the game's.roles_players dict and games's.teams_players dict.
        Only call once all players have been added"""

        shuffled_role_list = self.role_list
        random.shuffle(shuffled_role_list)

        for player in self.players.values():
            role_name = shuffled_role_list.pop()

            player.assign_role(role_name)

            self.roles_players[role_name].append(player)
            self.teams_players[player.role.team].append(player)

    # GAMEPLAY

    def number_alive(self, role_name=None, team_name=None, custom_player_list=None):
        """Returns an int, the number of remaining players of those specified that are still alive.
        The players under consideration can be chosen by role_name (str), team_name (str),
        or a custom_player_list (list).
        If run without arguments number_alive() returns the total number of players alive"""

        # Finds sets of players that meet each criteria, and counts the number of those that are in all sets
        # that are alive

        players = set(self.players.values())

        if role_name:
            players &= set(self.roles_players[role_name])

        if team_name:
            players &= set(self.teams_players[team_name])

        if custom_player_list:
            players &= set(custom_player_list)

        n = 0
        for player in players:
            n += player.alive

        return n


class Player:
    """For each player in the game, defined by discord ID # and name.
    Each player will have a role attribute"""

    def __init__(self, player_id, player_name):
        self.id = player_id
        self.name = player_name

        self.alive = True

        self.role = None

    def assign_role(self, role_name):
        """Updates the player's role, to an instance of the relevant role object"""

        # A dictionary of roles that are present, keys are names as strings, values are the role class objects
        available_roles = {role_class.__name__: role_class for role_class in Role.__subclasses__()}

        self.role = available_roles[role_name]()

    def kill(self):
        """Kills the player"""

        self.alive = False

        print(self.name, "has been killed, they were on the", self.role.team)


class Role:
    
    """The role for each player, with its own rules.
    Roles will have attributes & methods: team, team_appearance (eg. lycan), win_condition,
    first_night_behaviour, night_behaviour, night_order_precedence

    Some roles may have attributes modifiable for different rulesets,
    eg. bodyguard, can be able to protect self/not, can protect same person twice/not"""

    pass


class Villager(Role):
    """The villager role"""

    def __init__(self):
        self.team = 'villager_team'
        self.name = 'Villager'
        self.win_condition = None
        self.night_behaviour = None


class Werewolf(Role):
    """The werewolf role"""

    def __init__(self):
        self.team = 'werewolf_team'
        self.name = 'Werewolf'
        self.win_condition = None
        self.night_behaviour = None


class Seer(Role):
    """The seer role"""

    def __init__(self):
        self.team = 'villager_team'
        self.name = 'Seer'
        self.win_condition = None
        self.night_behaviour = None


if __name__ == "__main__":
    """Just for some testing and debugging. Sets up a game with players and assigns roles.
    Can kill players with player.kill(), can view players' statuses with game_state(),
    and can test numbers of different groups of players still alive with game.number_alive(...)"""
    game = WerewolfGame([('#1', 'Raph'), ('#2', 'Martin'), ('#3', 'Louis'), ('#4', 'Tom')])
    game.role_list = ['Villager', 'Villager', 'Seer', 'Werewolf']  # because not yet implemented in ruleset
    game.assign_roles()

    def game_state():
        print("id name     role.name role.team     alive")
        for player in game.players.values():
            print('{:2} {:8} {:9} {:13} {!s:5}'.format(player.id, player.name, player.role.name, player.role.team,
                                                       player.alive))

    game_state()
