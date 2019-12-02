
class WerewolfGame:
    """The class for the game engine.
    Will need to know the players (by discord ID # and name)
    And the ruleset - the roles in play, how many of each, and any modifiers"""

    pass

class Player:
    """For each player in the game, defined by discord ID # and name.
    Each player will have a role attribute"""

    pass

class Role:
    """The role for each player, with its own rules.
    Roles will have attributes & methods: team, team_appearance (eg. lycan), win_condition,
    first_night_behaviour, night_behaviour, night_order_precedence

    Some roles may have attributes modifiable for different rulesets,
    eg. bodyguard, can be able to protect self/not, can protect same person twice/not"""