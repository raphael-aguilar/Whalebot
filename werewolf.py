import random

class werewolf_game:
    """The class for the game engine.
    Will need to know the players (by discord ID # and name)
    And the ruleset - the roles in play, how many of each, and any modifiers"""

    def __init__(self, players, ruleset):

        # Need to sort out how we are identifying the players, discord ID#, discord name,
        # concatenation of both? eg. 'Martin#3769', or a tuple of both?
        # I'm just using a variable player_id for now

        self.player_list = []

        for player_id in players:
            self.add_player(player_id)

        # probably a dict of {'role':{modifier1:value, modifier2:value},...}, with each role in play included just once
        # most will just be empty/default, these can be the arguments for when the roles are initialised
        # self.role_modifiers = {}

        # list of roles in play, with each role occurring as many times as players with that role
        # self.role_list = []

    def add_player(self, player_id):
        """Add a new player to the game"""
        exec("{} = player({})".format(player_id, player_id))
        # Not sure if this is the best way to do this, I'm trying to create a player object named after each
        # player, with the player's name/id as an argument to then be an attribute

        self.player_list.append(exec(player_id))

    def assign_roles(self):
        """Shuffle the role_list and assign each player a random role"""
        pass


class player:
    """For each player in the game, defined by discord ID # and name.
    Each player will have a role attribute"""

    pass

class role:
    """The role for each player, with its own rules.
    Roles will have attributes & methods: team, team_appearance (eg. lycan), win_condition,
    first_night_behaviour, night_behaviour, night_order_precedence

    Some roles may have attributes modifiable for different rulesets,
    eg. bodyguard, can be able to protect self/not, can protect same person twice/not"""

    pass
