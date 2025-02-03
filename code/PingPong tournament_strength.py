import math
from functools import reduce

def win_probability(r1: float, r2: float) -> float:
    """
    Calculate the probability that a player with rating r1 defeats a player with rating r2.
    """
    return 1 / (1 + 10 ** ((r2 - r1) / 400))

def tournament_win_probability(player_ratings: list[float], avg_player_rating: float = 1500.0) -> float:
    """
    Calculate the cumulative probability of an average player winning the tournament by beating all players.

    Args:
        player_ratings (list[float]): Ratings of players in the tournament.
        avg_player_rating (float): Rating of the hypothetical average player (default: 1500).

    Returns:
        float: The cumulative probability of winning the tournament.
    """
    # Step 1: Compute probabilities of beating each player
    probabilities = [win_probability(avg_player_rating, r) for r in player_ratings]

    # Step 2: Compute the average win probability and raise it to the correct power
    avg_probability = sum(probabilities) / len(probabilities)
    p_all = avg_probability ** (len(player_ratings)-1)
    return p_all

def trating_from_p(p_win: float, avg_player_rating: float = 1500.0) -> float:
    """
    Solve for the opponent rating X such that Pwin(avg_player_rating, X) = p_win.

    Args:
        p_win (float): The target win probability.
        avg_player_rating (float): The rating of the player (default 1500).

    Returns:
        float: The solved opponent rating.
    """
    if not (0 < p_win < 1):
        raise ValueError("Probability must be between 0 and 1 (exclusive).")

    opponent_rating = avg_player_rating + 400 * math.log10((1 - p_win) / p_win)
    return opponent_rating

while False:
    elo_ratings = [1500,1500,1500,1500,1500]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1626.8,1920.2,1379.1,1485.1,1249.7]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1669.2,2006.6,1357.5,1131.6]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1763.7,	1891.1,	1246.8,1247.7]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1825.5,	1822.1,	1287.6, 1170.5]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1233.8, 1771.5,	1910.6,	1223.9]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1758.7,	1939.6,	1258.3,1500]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1729.9,	1916.9,	1247.3,2051.3]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1834.6, 1837.1,	1837.5,	1242.7]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1731.8, 1822.6,	1902.1,	1235.1]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1500, 1873.6,	1849.1]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1405.6, 1896.6,	1834.9]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1358.6, 1909.6,	1828.6]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1323.2, 1934.1,	1808.8]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1295.5, 1934.3,	1813.3]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1279.3,1944.5,1805.7]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")
    break

    elo_ratings = [1967.2,1500,1500]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1972.9,1605.1,1320.1]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1977.9,1619.8,1253.8]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1982,1518,1350.1]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1985.4,1479,1381.2]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1988.4,1459.8,1393.4]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")

    elo_ratings = [1990.9,1409.7,1438.4]
    probability = tournament_win_probability(elo_ratings, 1500.0)
    strength = trating_from_p(probability, 1500.0)
    print(f"Tournament Strength: {strength:.4f}")
    break