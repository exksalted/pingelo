#Imports
import csv
import math
import time



#Stuff to calculate ratings with:

Q = math.log(10) / 400

def g(rd):
    return 1 / math.sqrt(1 + 3 * (Q ** 2) * (rd ** 2) / (math.pi ** 2))

def expected_score(r, r_opponent, rd_opponent):
    g_rd = g(rd_opponent)
    return 1 / (1 + 10 ** (-g_rd * (r - r_opponent) / 400))

def calculate_new_rd(rd, d_squared):
    return math.sqrt(1 / (1 / (rd ** 2) + 1 / d_squared))

def calculate_new_rating(r, rd, results):
    d_squared_inv = sum(
        (g(op_rd) ** 2) * expected_score(r, op_r, op_rd) * (1 - expected_score(r, op_r, op_rd))
        for op_r, op_rd, _ in results
    )
    d_squared = 1 / (Q ** 2 * d_squared_inv)

    rating_update = sum(
        g(op_rd) * (actual - expected_score(r, op_r, op_rd))
        for op_r, op_rd, actual in results
    )
    r_new = r + Q / (1 / (rd ** 2) + 1 / d_squared) * rating_update

    rd_new = calculate_new_rd(rd, d_squared)
    return round(r_new, 1), round(rd_new, 1)

def update_ratings(player1, player2, score1, score2, players):
    r1, rd1 = players[player1]["rating"], players[player1]["rd"]
    r2, rd2 = players[player2]["rating"], players[player2]["rd"]

    if score1 > score2:
        score_factor1, score_factor2 = 1.0, 0.0  # Player 1 wins
    elif score1 < score2:
        score_factor1, score_factor2 = 0.0, 1.0  # Player 2 wins

    results1 = [(r2, rd2, score_factor1)]
    results2 = [(r1, rd1, score_factor2)]

    new_r1, new_rd1 = calculate_new_rating(r1, rd1, results1)
    new_r2, new_rd2 = calculate_new_rating(r2, rd2, results2)

    elo_change1 = round(new_r1 - r1, 1)
    elo_change2 = round(new_r2 - r2, 1)

    players[player1]["rating"], players[player1]["rd"] = new_r1, new_rd1
    players[player2]["rating"], players[player2]["rd"] = new_r2, new_rd2

    print(f"  New Ratings:")
    print(f"    {player1}: Rating = {new_r1} ({'+' if elo_change1 > 0 else ''}{elo_change1}), RD = {new_rd1}")
    print(f"    {player2}: Rating = {new_r2} ({'+' if elo_change2 > 0 else ''}{elo_change2}), RD = {new_rd2}")
    print("")



#Adding, loading and saving players' data

def add_player(file_name, player_name, ratingcsv, ratingcsvt, ratingcsvd):
    try:
        default_rating = 1500.0
        default_rd = 350.0

        # Add the player to the player data CSV
        with open(file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, default_rating, default_rd, 0, "", 0, "", "", 0, 0, "", 0, "", 0, 0, 0, 0, 0, 0, "", 0, "", 0, "", 0])
        print(f"Player '{player_name}' has been added to the file with rating {default_rating} and RD {default_rd}.")
        # Added: AVG Points, AVG Points against, Best WLMU Player, Best WLMU Score, Worst WLMU Player, Worst WLMU Score, Best ScoreMU player, Best ScoreMUS, Worst ScoreMU player, Worst ScoreMUS, Most played Player, Most played #
        # Open the ratingcsv to find the first empty column and last filled row
        with open(ratingcsv, "r", newline='') as file:
            reader = list(csv.reader(file))

            # Initialize file if empty
            if not reader:
                header = [player_name]
                row = [default_rating]
            else:
                # Find the header and first empty column
                header = reader[0]
                player_col_index = len(header)

                for i, column_name in enumerate(header):
                    if not column_name:  # Empty column found
                        player_col_index = i
                        break

                # Update header if new column required
                if player_col_index == len(header):
                    header.append(player_name)

                # Find the last filled row
                last_row_index = max(i for i, row in enumerate(reader) if any(row))
                last_row = reader[last_row_index]

                # Ensure row has enough columns and add player rating
                while len(last_row) < len(header):
                    last_row.append("")
                last_row[player_col_index] = str(default_rating)

        # Write the updated data back to the file
        with open(ratingcsv, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            if not reader:
                writer.writerow(row)
            else:
                writer.writerows(reader[1:last_row_index])  # Skip incomplete rows
                writer.writerow(last_row)  # Write the last updated row

      # Open the ratingcsvt to find the first empty column and last filled row
        with open(ratingcsvt, "r", newline='') as file:
            reader = list(csv.reader(file))

            # Initialize file if empty
            if not reader:
                header = [player_name]
                row = [default_rating]
            else:
                # Find the header and first empty column
                header = reader[0]
                player_col_index = len(header)

                for i, column_name in enumerate(header):
                    if not column_name:  # Empty column found
                        player_col_index = i
                        break

                # Update header if new column required
                if player_col_index == len(header):
                    header.append(player_name)

                # Find the last filled row
                last_row_index = max(i for i, row in enumerate(reader) if any(row))
                last_row = reader[last_row_index]

                # Ensure row has enough columns and add player rating
                while len(last_row) < len(header):
                    last_row.append("")
                last_row[player_col_index] = str(default_rating)

        # Write the updated data back to the file
        with open(ratingcsvt, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            if not reader:
                writer.writerow(row)
            else:
                writer.writerows(reader[1:last_row_index])  # Skip incomplete rows
                writer.writerow(last_row)  # Write the last updated row

        # Open the ratingcsvd to find the first empty column and last filled row
        with open(ratingcsvd, "r", newline='') as file:
            reader = list(csv.reader(file))

            # Initialize file if empty
            if not reader:
                header = [player_name]
                row = [default_rating]
            else:
                # Find the header and first empty column
                header = reader[0]
                player_col_index = len(header)

                for i, column_name in enumerate(header):
                    if not column_name:  # Empty column found
                        player_col_index = i
                        break

                # Update header if new column required
                if player_col_index == len(header):
                    header.append(player_name)

                # Find the last filled row
                last_row_index = max(i for i, row in enumerate(reader) if any(row))
                last_row = reader[last_row_index]

                # Ensure row has enough columns and add player rating
                while len(last_row) < len(header):
                    last_row.append("")
                last_row[player_col_index] = str(default_rating)

        # Write the updated data back to the file
        with open(ratingcsvd, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            if not reader:
                writer.writerow(row)
            else:
                writer.writerows(reader[1:last_row_index])  # Skip incomplete rows
                writer.writerow(last_row)  # Write the last updated row

    except Exception as e:
        print(f"An error occurred: {e}")

def load_players(filename):
    players = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            name = row[0]
            players[name] = {
                "rating": float(row[1]) if row[1] else 0.0,
                "rd": float(row[2]) if row[2] else 0.0,
                "rd_change": float(row[3]) if len(row) > 3 and row[3] else 0.0,
                "current_rank": int(row[4]) if len(row) > 4 and row[4] else 0,
                "rank_change": int(row[5]) if len(row) > 5 and row[5] else 0,
                "peak_rank": int(row[6]) if len(row) > 6 and row[6] else 0,
                "lowest_rank": int(row[7]) if len(row) > 7 and row[7] else 0,
                "tournaments_played": int(row[8]) if len(row) > 8 and row[8] else 0,
                "best_victory_rating": float(row[9]) if len(row) > 9 and row[9] else 0.0,
                "bv_player": row[10] if len(row) > 10 else '',
                "worst_defeat_rating": float(row[11]) if len(row) > 11 and row[11] else 0.0,
                "wd_player": row[12] if len(row) > 12 else '',
                "lumiw": int(row[13]) if len(row) > 13 and row[14] else 0,
                "loskaw": int(row[14]) if len(row) > 14 and row[14] else 0,
                "lumil": int(row[15]) if len(row) > 15 and row[15] else 0,
                "loskal": int(row[16]) if len(row) > 16 and row[16] else 0,
                # Added: AVG Points, AVG Points against, Best WLMU Player, Best WLMU Score, Worst WLMU Player, Worst WLMU Score, Most played Player, Most played #
                "avgpoints": float(row[17]) if len(row) > 17 and row[17] else 0.00,
                "avgp_opp": float(row[18]) if len(row) > 18 and row[18] else 0.00,
                "BWLMUP": row[19] if len(row) > 19 and row[19] else 0,
                "BWLMUS": row[20] if len(row) > 20 and row[20] else 0,
                "WWLMUP": row[21] if len(row) > 21 and row[21] else 0,
                "WWLMUS": row[22] if len(row) > 22 and row[22] else 0,
                "MPP":    row[23] if len(row) > 23 and row[23] else 0,
                "MPN":    int(row[24]) if len(row) > 24 and row[24] else 0
            }
    return players

def load_rating_csv_header(ratingcsv):
    """Loads the header from the rating CSV to maintain column order."""
    with open(ratingcsv, "r") as file:
        reader = csv.reader(file)
        return next(reader, [])

def save_players_to_file(filename, players):
    try:
        sorted_players = sorted(players.items(), key=lambda x: x[1]["rating"], reverse=True)
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            for name, data in sorted_players:
                row = [
                    name, 
                    data["rating"], 
                    data["rd"], 
                    data.get("rd_change", 0),
                    data.get("current_rank", 0), 
                    data.get("rank_change", 0),
                    data.get("peak_rank", 0), 
                    data.get("lowest_rank", 0),
                    data.get("tournaments_played", 0), 
                    data.get("best_victory_rating", 0),
                    data.get("bv_player", ""), 
                    data.get("worst_defeat_rating", 0), 
                    data.get("wd_player", ""),
                    data.get("lumiw", 0),
                    data.get("loskaw", 0), 
                    data.get("lumil", 0),
                    data.get("loskal", 0),
                    data.get("avgpoints", 0),
                    data.get("avgp_opp", 0),
                    data.get("BWLMUP", 0),
                    data.get("BWLMUS", 0),
                    data.get("WWLMUP", 0),
                    data.get("WWLMUS", 0),
                    data.get("MPP", 0),
                    data.get("MPN", 0)
                ]
                writer.writerow(row)
    except Exception as e:
        print(f"An error occurred while saving players: {e}")



#Functions for calculating tournament strength:

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



#Functions for running match stats, including calculating increase in RD, running matches, tourneys and sets of tourneys.

def adjust_rd(filename, days):
    try:
        players = load_players(filename)  # Reuse existing player loading function

        # Compute median RD for players with RD < 175
        rds = [player["rd"] for player in players.values() if player["rd"] < 175]
        if not rds:
            print("No players with RD under 175 found.")
            return

        rds.sort()
        n = len(rds)
        median_rd = rds[n // 2] if n % 2 == 1 else (rds[n // 2 - 1] + rds[n // 2]) / 2

        print("\n" + "*" * 50)
        print("Updating player RD values")
        print(f"Median RD: {median_rd}")

        c = math.sqrt((350 ** 2 - median_rd ** 2) / 365)
        print(f"Decay factor (c): {c}\n")

        # Update RD for each player
        for player_name, player_data in players.items():
            old_rd = player_data["rd"]
            new_rd = math.sqrt(old_rd ** 2 + c ** 2 * days)
            players[player_name]["rd"] = min(new_rd, 350)
            print(f"Updated {player_name}'s RD from {old_rd:.2f} to {new_rd:.2f}")

        # Save the updated players back to the file
        save_players_to_file(filename, players)

        print("\nPlayer RD values have been updated.")
        print("*" * 50)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_match(matchdata, ratingcsv, playerdata):
    try:
        # Split match data to extract player names and scores
        player1_name, player2_name, score1, score2 = matchdata.split()
        score1, score2 = int(score1), int(score2)

        # Load current player data from playerdata CSV
        players = load_players(playerdata)

        # Ensure both players exist in the file
        if player1_name not in players or player2_name not in players:
            missing_players = [p for p in [player1_name, player2_name] if p not in players]
            raise ValueError(f"Missing players in data: {', '.join(missing_players)}")

        # Store pre-match ratings for both players
        player1_pre_rating = players[player1_name]["rating"]
        player2_pre_rating = players[player2_name]["rating"]

        # Update player ratings and RD values
        update_ratings(player1_name, player2_name, score1, score2, players)

        # LumiW and LumiL logic for perfect wins or losses
        if (score1 == 6 and score2 == 0) or (score2 == 6 and score1 == 0):
            if score1 == 6:  # Player 1 wins 6-0
                players[player1_name]["lumiw"] += 1
                players[player2_name]["lumil"] += 1
            elif score2 == 6:  # Player 2 wins 6-0
                players[player2_name]["lumiw"] += 1
                players[player1_name]["lumil"] += 1

        # LoskaW and LoskaL logic for dominant wins or losses
        if (score1 == 9 and score2 == 1) or (score2 == 9 and score1 == 1):
            if score1 == 9:  # Player 1 wins 9-1
                players[player1_name]["loskaw"] += 1
                players[player2_name]["loskal"] += 1
            elif score2 == 9:  # Player 2 wins 9-1
                players[player2_name]["loskaw"] += 1
                players[player1_name]["loskal"] += 1

        # Update Best Victory Rating and BV Player for the winner
        if score1 > score2:  # Player 1 wins
            if player2_pre_rating > players[player1_name]["best_victory_rating"]:
                players[player1_name]["best_victory_rating"] = player2_pre_rating
                players[player1_name]["bv_player"] = player2_name
        elif score2 > score1:  # Player 2 wins
            if player1_pre_rating > players[player2_name]["best_victory_rating"]:
                players[player2_name]["best_victory_rating"] = player1_pre_rating
                players[player2_name]["bv_player"] = player1_name

        # Update Worst Defeat Rating and WD Player for the loser
        if score1 < score2:  # Player 1 loses
            if (players[player1_name]["worst_defeat_rating"] == 0 or
                player2_pre_rating < players[player1_name]["worst_defeat_rating"]):
                players[player1_name]["worst_defeat_rating"] = player2_pre_rating
                players[player1_name]["wd_player"] = player2_name
        elif score2 < score1:  # Player 2 loses
            if (players[player2_name]["worst_defeat_rating"] == 0 or
                player1_pre_rating < players[player2_name]["worst_defeat_rating"]):
                players[player2_name]["worst_defeat_rating"] = player1_pre_rating
                players[player2_name]["wd_player"] = player1_name

        # Save updated data back to playerdata
        save_players_to_file(playerdata, players)

        # Append the updated ratings to the rating CSV file
        with open(ratingcsv, "a", newline='') as file:
            writer = csv.writer(file)
            # Extract player ratings in the order of the current header
            current_ratings = [players.get(name, {}).get("rating", "") for name in load_rating_csv_header(ratingcsv)]
            writer.writerow(current_ratings)

        print(f"Ratings updated successfully for match: {player1_name} vs {player2_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_tournament(input_file, output_file):
    # Read the existing stats from the output file (if any)
    stats = {}
    try:
        with open(output_file, 'r') as out_file:
            current_player = None
            for line in out_file:
                if line.startswith("  vs "):  # Pairwise stats line
                    if current_player is not None:
                        parts = line.strip().split(',')
                        opponent = parts[0].split('vs ')[1].strip()
                        wins_against = int(parts[1].split(': ')[1])
                        losses_to = int(parts[2].split(': ')[1])
                        avg_points_scored = float(parts[3].split(': ')[1])
                        avg_points_against = float(parts[4].split(': ')[1])
                        games = wins_against + losses_to

                        if opponent not in stats[current_player]['opponents']:
                            stats[current_player]['opponents'][opponent] = {
                                'wins_against': 0, 'losses_to': 0,
                                'total_points_scored': 0, 'total_points_against': 0, 'games': 0
                            }
                        opp_stats = stats[current_player]['opponents'][opponent]
                        opp_stats['wins_against'] += wins_against
                        opp_stats['losses_to'] += losses_to
                        opp_stats['total_points_scored'] += avg_points_scored * games
                        opp_stats['total_points_against'] += avg_points_against * games
                        opp_stats['games'] += games
                else:  # Main stats line
                    parts = line.strip().split(',')
                    if len(parts) == 6:  # Updated to include avg_opponent_points
                        player = parts[0]
                        wins = int(parts[1])
                        losses = int(parts[2])
                        wl_ratio = float(parts[3])
                        avg_points = float(parts[4])
                        avg_opponent_points = float(parts[5])
                        stats[player] = {
                            'wins': wins, 'losses': losses,
                            'total_points': avg_points * (wins + losses),
                            'total_opponent_points': avg_opponent_points * (wins + losses),
                            'opponents': {}
                        }
                        current_player = player
    except FileNotFoundError:
        pass  # If the output file doesn't exist, we create it later

    # Process the input tournament file
    with open(input_file, 'r') as in_file:
        for line in in_file:
            parts = line.strip().split()
            if len(parts) == 4:  # Assuming format: Player1, Player2, PointsPlayer1, PointsPlayer2
                player1, player2, points1, points2 = parts
                points1 = int(points1)
                points2 = int(points2)

                # Adjust scores based on the rules
                if points1 == 6 and points2 == 0:
                    points1 = 11
                elif points2 == 6 and points1 == 0:
                    points2 = 11
                elif points1 == 9 and points2 == 1:
                    points1 = 11
                elif points2 == 9 and points1 == 1:
                    points2 = 11
                elif points1 >= 10 and points2 >= 10 and points1 > points2:
                    points2 = (points2 / points1) * 11
                    points1 = 11
                elif points1 >= 10 and points2 >= 10 and points2 > points1:
                    points1 = (points1 / points2) * 11
                    points2 = 11

                # Ensure both players have an entry in the stats dictionary
                if player1 not in stats:
                    stats[player1] = {'wins': 0, 'losses': 0, 'total_points': 0, 'total_opponent_points': 0, 'opponents': {}}
                if player2 not in stats:
                    stats[player2] = {'wins': 0, 'losses': 0, 'total_points': 0, 'total_opponent_points': 0, 'opponents': {}}

                # Ensure pairwise stats are initialized
                if player2 not in stats[player1]['opponents']:
                    stats[player1]['opponents'][player2] = {'wins_against': 0, 'losses_to': 0, 'total_points_scored': 0, 'total_points_against': 0, 'games': 0}
                if player1 not in stats[player2]['opponents']:
                    stats[player2]['opponents'][player1] = {'wins_against': 0, 'losses_to': 0, 'total_points_scored': 0, 'total_points_against': 0, 'games': 0}

                # Update stats for Player 1 and Player 2
                if points1 > points2:
                    stats[player1]['wins'] += 1
                    stats[player2]['losses'] += 1
                    stats[player1]['opponents'][player2]['wins_against'] += 1
                    stats[player2]['opponents'][player1]['losses_to'] += 1
                else:
                    stats[player1]['losses'] += 1
                    stats[player2]['wins'] += 1
                    stats[player1]['opponents'][player2]['losses_to'] += 1
                    stats[player2]['opponents'][player1]['wins_against'] += 1

                # Update points and games
                stats[player1]['total_points'] += points1
                stats[player2]['total_points'] += points2
                stats[player1]['total_opponent_points'] += points2
                stats[player2]['total_opponent_points'] += points1
                stats[player1]['opponents'][player2]['total_points_scored'] += points1
                stats[player1]['opponents'][player2]['total_points_against'] += points2
                stats[player1]['opponents'][player2]['games'] += 1
                stats[player2]['opponents'][player1]['total_points_scored'] += points2
                stats[player2]['opponents'][player1]['total_points_against'] += points1
                stats[player2]['opponents'][player1]['games'] += 1

    # Calculate the final WL ratio, average points, and average opponent points
    for player in stats:
        total_games = stats[player]['wins'] + stats[player]['losses']
        if total_games > 0:
            wl_ratio = stats[player]['wins'] / total_games
            avg_points = stats[player]['total_points'] / total_games
            avg_opponent_points = stats[player]['total_opponent_points'] / total_games
        else:
            wl_ratio = 0
            avg_points = 0
            avg_opponent_points = 0
        stats[player]['wl_ratio'] = wl_ratio
        stats[player]['avg_points'] = avg_points
        stats[player]['avg_opponent_points'] = avg_opponent_points

        # Calculate pairwise stats
        for opponent in stats[player]['opponents']:
            pairwise_stats = stats[player]['opponents'][opponent]
            pairwise_stats['avg_points_scored'] = pairwise_stats['total_points_scored'] / pairwise_stats['games'] if pairwise_stats['games'] > 0 else 0
            pairwise_stats['avg_points_against'] = pairwise_stats['total_points_against'] / pairwise_stats['games'] if pairwise_stats['games'] > 0 else 0

    # Write the updated stats to the output file (overwrite the file)
    with open(output_file, 'w') as out_file:
        for player, player_stats in stats.items():
            out_file.write(f"{player},{player_stats['wins']},{player_stats['losses']},{player_stats['wl_ratio']},{player_stats['avg_points']},{player_stats['avg_opponent_points']}\n")
            for opponent, pairwise_stats in player_stats['opponents'].items():
                out_file.write(f"  vs {opponent}, Wins: {pairwise_stats['wins_against']}, Losses: {pairwise_stats['losses_to']}, "
                               f"Avg Points Scored: {pairwise_stats['avg_points_scored']}, Avg Points Against: {pairwise_stats['avg_points_against']}\n")

def run_tournament(tournament_file, playerfile, ratingcsv, rating_csv_t, player_stats):
    # Process the tournament and update player stats
    process_tournament(tournament_file, player_stats)

    try:
        # Open and read the tournament file
        with open(tournament_file, "r") as file:
            matches = file.readlines()

        # Extract unique player names from matches
        unique_players = set()
        valid_matches = []

        for matchdata in matches:
            matchdata = matchdata.strip()
            # Skip lines indicating tournament strength
            if matchdata.startswith("Tournament Strength:"):
                continue
            if matchdata:
                player1_name, player2_name, *_ = matchdata.split()
                unique_players.update([player1_name, player2_name])
                valid_matches.append(matchdata)

        # Only proceed if the tournament is valid (at least 4 unique players)
        valid_tournament = len(unique_players) >= 4

        # Calculate tournament strength before processing matches if valid
        players = load_players(playerfile)

        if valid_tournament:
            player_ratings = [players[player]["rating"] for player in unique_players if player in players]
            if player_ratings:
                p_win = tournament_win_probability(player_ratings)
                tournament_strength = trating_from_p(p_win)

                # Append tournament strength to the tournament file
                with open(tournament_file, "a") as file:
                    file.write(f"\nTournament Strength: {tournament_strength:.2f}\n")

                print(f"\nTournament strength ({tournament_strength:.2f}) calculated and appended to {tournament_file}.")

        # Run each valid match in the tournament
        for matchdata in valid_matches:
            run_match(matchdata, ratingcsv, playerfile)

        # Reload players after tournament matches
        players = load_players(playerfile)

        # Rank players by rating (highest rating is rank 1)
        ranked_players = sorted(players.items(), key=lambda x: x[1]["rating"], reverse=True)

        print("\nUpdating ranks and tournament counts for players:")
        for rank, (player_name, player_data) in enumerate(ranked_players, start=1):
            # Update current rank
            player_data["current_rank"] = rank

            # Handle peak and lowest rank logic
            if player_data["peak_rank"] == 0 or rank < player_data["peak_rank"]:
                player_data["peak_rank"] = rank

            if player_data["lowest_rank"] == 0 or rank > player_data["lowest_rank"]:
                player_data["lowest_rank"] = rank

            # Increment tournaments played only for players who participated
            if valid_tournament and player_name in unique_players:
                player_data["tournaments_played"] += 1

            print(f"{player_name}: Current Rank = {rank}, Peak Rank = {player_data['peak_rank']}, "
                  f"Lowest Rank = {player_data['lowest_rank']}, Tournaments Played = {player_data['tournaments_played']}")

        # Save updated player data back to player file
        save_players_to_file(playerfile, players)

        # Append current ratings to the ratings_csv_t file
        with open(rating_csv_t, "a", newline='') as file:
            writer = csv.writer(file)
            # Write the current ratings for all players in the order of the header
            header = load_rating_csv_header(rating_csv_t)
            current_ratings = [players.get(name, {}).get("rating", "") for name in header]
            writer.writerow(current_ratings)

        print("\nTournament processed successfully, player ranks and tournament counts updated.")
        print(f"Current ratings appended to {rating_csv_t}.")

    except FileNotFoundError:
        print(f"The file {tournament_file} was not found.")
    except Exception as e:
        print(f"An error occurred during the tournament: {e}")

def run_tournament_set(t_list, player_file, ratings_csv, ratings_csv_t, ratings_csv_d, player_stats, days=0):
    try:
        # Load initial player data and save current RD and ranks locally
        players = load_players(player_file)
        initial_rd_ranks = {player: {"rd": data["rd"], "rank": data["current_rank"]} for player, data in players.items()}

        # Adjust RD only if days > 0
        if days > 0:
            adjust_rd(player_file, days)  # Pass the player file path, not the dict

        # Run each tournament in the list
        for tournament_file in t_list:
            run_tournament(tournament_file, player_file, ratings_csv, ratings_csv_t, player_stats)

        # Reload player data to capture final RD and ranks after tournaments
        updated_players = load_players(player_file)

        # Calculate RD and rank changes
        for player, data in updated_players.items():
            initial_rd = initial_rd_ranks.get(player, {}).get("rd", data["rd"])
            initial_rank = initial_rd_ranks.get(player, {}).get("rank", data["current_rank"])

            # Update RD change
            rd_change = round(data["rd"] - initial_rd, 2)
            updated_players[player]["rd_change"] = rd_change

            # Update rank change
            rank_change = data["current_rank"] - initial_rank
            updated_players[player]["rank_change"] = rank_change

        # Save updated data back to player file
        save_players_to_file(player_file, updated_players)

        #Run matchup stats
        matchup_stats(player_stats, player_file)

        # Append current ratings to the ratings_csv_d file
        with open(ratings_csv_d, "a", newline='') as file:
            writer = csv.writer(file)
            # Write the current ratings for all players in the order of the header
            header = load_rating_csv_header(ratings_csv_d)
            current_ratings = [updated_players.get(name, {}).get("rating", "") for name in header]
            writer.writerow(current_ratings)

        print(f"Tournament set successfully processed. RD and rank changes updated.")
        print(f"Current ratings appended to {ratings_csv_d}.")

    except Exception as e:
        print(f"An error occurred: {e}")

def matchup_stats(txt_file, csv_file):
    """
    Reads player matchup statistics from a text file and updates corresponding entries in a CSV file.
    """
    try:
        # Load players from the CSV file
        players = load_players(csv_file)

        with open(txt_file, "r") as file:
            lines = file.readlines()

        current_player = None
        match_counts = {}  # Track match counts for each player

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Identify the main player and their stats
            if "," in line and "vs" not in line:
                parts = line.split(",")
                current_player = parts[0].strip()
                avg_points = float(parts[4].strip()) if len(parts) > 4 else 0.0
                avg_points_opp = float(parts[5].strip()) if len(parts) > 5 else 0.0

                if current_player in players:
                    players[current_player]["avgpoints"] = avg_points
                    players[current_player]["avgp_opp"] = avg_points_opp
                    match_counts[current_player] = {}

            # Process each matchup entry for the current player
            elif current_player and "vs" in line:
                parts = line.split(",")
                opponent = parts[0].replace("vs", "").strip()

                # Extract wins and losses
                wins = int(parts[1].split(":")[-1].strip())
                losses = int(parts[2].split(":")[-1].strip())
                total_matches = wins + losses

                if opponent:
                    match_counts[current_player][opponent] = (wins, losses)

        # Update most played player and match count, best/worst WL matchups
        for player, opponents in match_counts.items():
            if opponents:
                # Most played player and count
                most_played_opponent = max(opponents, key=lambda k: sum(opponents[k]))
                most_played_count = sum(opponents[most_played_opponent])
                players[player]["MPP"] = most_played_opponent
                players[player]["MPN"] = most_played_count

                # Best WL matchup (highest win percentage, break ties by total matches)
                best_wl_opponent = max(
                opponents, key=lambda k: (opponents[k][0] / max(1, sum(opponents[k])), sum(opponents[k]))
                )

                # Worst WL matchup (smallest win ratio, tie-break by total matches)
                worst_wl_opponent = min(
                opponents, key=lambda k: (opponents[k][0] / max(1, sum(opponents[k])), -sum(opponents[k]))
                )

                best_wl_stats = f"{opponents[best_wl_opponent][0]} - {opponents[best_wl_opponent][1]}"
                worst_wl_stats = f"{opponents[worst_wl_opponent][0]} - {opponents[worst_wl_opponent][1]}"

                players[player]["BWLMUP"] = best_wl_opponent
                players[player]["BWLMUS"] = best_wl_stats
                players[player]["WWLMUP"] = worst_wl_opponent
                players[player]["WWLMUS"] = worst_wl_stats


        # Save updated player data back to the CSV file
        save_players_to_file(csv_file, players)

        print("Player matchup statistics successfully updated.")

    except FileNotFoundError:
        print(f"The file {txt_file} or {csv_file} was not found.")
    except Exception as e:
        print(f"An error occurred while updating matchup statistics: {e}")


#Running the code:

pf = "data_player.csv"
rcsv = "data_ratingsM.csv"
rcsvt = "data_ratingsT.csv"
rcsvd = "data_ratingsD.csv"
player_stats = "data_stats.txt"

while True:
    start_time = time.time()
    add_player(pf, "Aaro", rcsv, rcsvt, rcsvd)
    add_player(pf, "Juho", rcsv, rcsvt, rcsvd)
    add_player(pf, "Riku", rcsv, rcsvt, rcsvd)
    add_player(pf, "Matias", rcsv, rcsvt, rcsvd)
    add_player(pf, "Tuomas", rcsv, rcsvt, rcsvd)
    tournament_list = ["P11.txt", "P12.txt", "P13.txt", "P14.txt", "P15.txt", "P16.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 0)

    add_player(pf, "Jesper", rcsv, rcsvt, rcsvd)
    tournament_list = ["P21.txt", "P22.txt", "P23.txt", "P24.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 5)

    add_player(pf, "Jussi", rcsv, rcsvt, rcsvd)
    tournament_list = ["P31.txt", "P32.txt", "P33.txt", "P34.txt", "P35.txt", "P36.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 4)

    tournament_list = ["P41.txt", "P42.txt", "P43.txt", "P44.txt", "P45.txt", "P46.txt", "P47.txt", "P48.txt", "P49.txt", "P410.txt", "P411.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 7)

    tournament_list = ["P51.txt", "P52.txt", "P53.txt", "P54.txt", "P55.txt", "P56.txt", "P57.txt", "P58.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 3)

    add_player(pf, "Samuel", rcsv, rcsvt, rcsvd)
    add_player(pf, "Elias", rcsv, rcsvt, rcsvd)
    tournament_list =["R11.txt", "R12.txt", "R13.txt", "R14.txt", "R15.txt", "R16.txt", "R17.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 2)

    tournament_list = ["P61.txt", "P62.txt", "P63.txt", "P64.txt", "P65.txt", "P66.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 2)

    tournament_list = ["P71.txt"]
    run_tournament_set(tournament_list, pf, rcsv, rcsvt, rcsvd, player_stats, 2)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Calculated stats in {elapsed_time:.6f} seconds")
    break