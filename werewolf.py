import random
import discord


class WerewolfGame:
    """The class for the game engine.
    Will need to know the players (by discord ID # and name)
    And the ruleset - the roles in play, how many of each, and any modifiers"""

    def __init__(self, player_list, ruleset=None):
        """Takes a list of tuples for players, the tuples will be (player_id, player_name)"""

        # Need to sort out how we are identifying the players, discord ID#, discord name,
        # concatenation of both? eg. 'Martin#3769', or a tuple of both?
        # I'm just using a variable player_id for now

        # a dictionary of player objects, with their player_id as the keys
        self.players = {}

        for player_id, player_name in player_list:
            self.add_player(player_id, player_name)

        # probably a dict of {'role':{modifier1:value, modifier2:value},...}, with each role in play included just once
        # most will just be empty/default, these can be the arguments for when the roles are initialised
        # self.role_modifiers = {}
        self.roles = {}

        # list of roles in play, with each role occurring as many times as players with that role
        self.role_list = []

    def add_player(self, player_id, player_name):
        """Add a new player to the game
        Separate of __init__ so that this can be called separately"""

        self.players[player_id] = Player(player_id, player_name)

    def assign_roles(self):
        """Shuffle the role_list and assign each player a random role
        Call once all players have been added"""

        shuffled_role_list = self.role_list
        random.shuffle(shuffled_role_list)

        for player in self.players.values():
            player.assign_role(shuffled_role_list.pop())


class Player:
    """For each player in the game, defined by discord ID # and name.
    Each player will have a role attribute"""

    def __init__(self, player_id, player_name):
        self.id = player_id
        self.name = player_name

        self.role = None

    def assign_role(self, role):
        self.role = role


class Role:
    """The role for each player, with its own rules.
    Roles will have attributes & methods: team, team_appearance (eg. lycan), win_condition,
    first_night_behaviour, night_behaviour, night_order_precedence

    Some roles may have attributes modifiable for different rulesets,
    eg. bodyguard, can be able to protect self/not, can protect same person twice/not"""

    pass


class Villager(Role):

    pass


class Werewolf(Role):

    pass


class Seer(Role):

    pass
