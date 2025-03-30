"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    total = 0
    has_one = False  # Flag to check if any roll is 1

    for _ in range(num_rolls):
        roll = dice()  # Roll the dice
        if roll == 1:
            has_one = True
        total += roll

    # Return 1 if any roll was 1, otherwise return the sum
    return 1 if has_one else total


def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    player_digit = player_score % 10
    opponent_tens = (opponent_score // 10) % 10
    difference = abs(opponent_tens - player_digit)
    points = 3 * difference
    return max(points, 1)


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    return roll_dice(num_rolls, dice)


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    turn_points = take_turn(num_rolls, player_score, opponent_score, dice)
    return player_score + turn_points


def is_prime(n):
    """Return whether N is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""
    factors = 0
    for k in range(1, n + 1):
        if n % k == 0:
            factors += 1
    return factors


def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    factor_count = num_factors(score)
    if factor_count in [3, 4]:
        for i in range(score + 1, 110):
            if is_prime(i):
                return i
    return score


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    turn_points = take_turn(num_rolls, player_score, opponent_score, dice)
    new_score = player_score + turn_points
    return sus_points(new_score)


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    while score0 < goal and score1 < goal:
        if who == 0:
            # 玩家0的回合
            num_rolls = strategy0(score0, score1)
            score0 = update(num_rolls, score0, score1, dice)
        else:
            # 玩家1的回合
            num_rolls = strategy1(score1, score0)
            score1 = update(num_rolls, score1, score0, dice)
        # 切换玩家
        who = 1 - who
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10

    def strategy(player_score, opponent_score):
        return n

    return strategy


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> catch_up(17, 18)
    6
    """
    return 6 if score < opponent_score else 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    base = strategy(0, 0)
    for score in range(goal + 1):
        for opp in range(goal + 1):
            if strategy(score, opp) != base:
                return False
    return True


def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """

    def averaged(*args):
        total = 0
        for _ in range(times_called):
            total += original_function(*args)
        return total / times_called

    return averaged


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    max_avg = -1
    best_roll = 1
    avg = make_averaged(roll_dice, times_called)
    for num in range(1, 11):
        current = avg(num, dice)
        if current > max_avg:
            max_avg = current
            best_roll = num
    return best_roll


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    return 0 if score0 > score1 else 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_count_0 = 0
    win_count_1 = 0
    times = 1000
    for _ in range(times):
        if winner(strategy, baseline) == 0:
            win_count_0 += 1
        if winner(baseline, strategy) == 1:
            win_count_1 += 1
    return (win_count_0 + win_count_1) / (2 * times)


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6)))  # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    potential = boar_brawl(score, opponent_score)
    return 0 if potential >= threshold else num_rolls


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    after_zero = sus_update(0, score, opponent_score, six_sided)
    return 0 if (after_zero - score) >= threshold else num_rolls


def final_strategy(score, opponent_score):
    """
    最终策略描述：
    1. 如果通过 Boar Brawl 规则能获得至少 12 分，选择掷 0 个骰子。
    2. 如果当前分数接近目标分数（如大于 90 分），为了尽快达到目标，选择掷 6 个骰子。
    3. 如果对手分数接近目标分数（如大于 90 分），为了追赶或超越对手，选择掷 6 个骰子。
    4. 其他情况默认掷 5 个骰子。
    """
    if boar_brawl(score, opponent_score) >= 12:
        return 0
    if score > 90:
        return 6
    if opponent_score > 90:
        return 6
    return 5


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()