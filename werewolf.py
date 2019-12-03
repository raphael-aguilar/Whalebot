import random
import discord


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
        # self.role_modifiers = {}

        # list of roles in play, with each role occurring as many times as players with that role
        self.role_list = []

    def add_player(self, player_id, player_name):
        """Add a new player to the game"""

        self.players[player_id] = Player(player_id, player_name)

    def assign_roles(self):
        """Shuffle the role_list and assign each player a random role
        Call once all players have been added"""

        shuffled_role_list = self.role_list
        random.shuffle(shuffled_role_list)

        for player in self.players.values():
            player.assign_role(shuffled_role_list.pop())

        ##To implement: lists of players of each role, eg. werewolves = []

    # GAMEPLAY

    def number_role_alive(self, role_name):
        """Returns an int, the number of remaining players of the role specified that are still alive"""
        ##To implement: make this function more general, eg. number_alive(role='Werewolf'), number_alive(team=...)

        n = 0

        for player in self.players.values():
            if player.role.name == role_name:
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
        available_roles = {cls.__name__: cls for cls in Role.__subclasses__()}

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
    game = WerewolfGame([('#1', 'Raph'), ('#2', 'Martin'), ('#3', 'Louis'), ('#4', 'Tom')])
    game.role_list = ['Villager', 'Villager', 'Seer', 'Werewolf']  # because not yet implemented in ruleset
    game.assign_roles()

