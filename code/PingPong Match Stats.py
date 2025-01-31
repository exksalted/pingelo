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
                    if len(parts) == 5:
                        player = parts[0]
                        wins = int(parts[1])
                        losses = int(parts[2])
                        wl_ratio = float(parts[3])
                        avg_points = float(parts[4])
                        stats[player] = {
                            'wins': wins, 'losses': losses,
                            'total_points': avg_points * (wins + losses),
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
                    stats[player1] = {'wins': 0, 'losses': 0, 'total_points': 0, 'opponents': {}}
                if player2 not in stats:
                    stats[player2] = {'wins': 0, 'losses': 0, 'total_points': 0, 'opponents': {}}

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
                stats[player1]['opponents'][player2]['total_points_scored'] += points1
                stats[player1]['opponents'][player2]['total_points_against'] += points2
                stats[player1]['opponents'][player2]['games'] += 1
                stats[player2]['opponents'][player1]['total_points_scored'] += points2
                stats[player2]['opponents'][player1]['total_points_against'] += points1
                stats[player2]['opponents'][player1]['games'] += 1

    # Calculate the final WL ratio and average points
    for player in stats:
        total_games = stats[player]['wins'] + stats[player]['losses']
        if total_games > 0:
            wl_ratio = stats[player]['wins'] / total_games
        else:
            wl_ratio = 0
        avg_points = stats[player]['total_points'] / total_games if total_games > 0 else 0
        stats[player]['wl_ratio'] = wl_ratio
        stats[player]['avg_points'] = avg_points

        # Calculate pairwise stats
        for opponent in stats[player]['opponents']:
            pairwise_stats = stats[player]['opponents'][opponent]
            pairwise_stats['avg_points_scored'] = pairwise_stats['total_points_scored'] / pairwise_stats['games'] if pairwise_stats['games'] > 0 else 0
            pairwise_stats['avg_points_against'] = pairwise_stats['total_points_against'] / pairwise_stats['games'] if pairwise_stats['games'] > 0 else 0

    # Write the updated stats to the output file (overwrite the file)
    with open(output_file, 'w') as out_file:
        for player, player_stats in stats.items():
            out_file.write(f"{player},{player_stats['wins']},{player_stats['losses']},{player_stats['wl_ratio']},{player_stats['avg_points']}\n")
            for opponent, pairwise_stats in player_stats['opponents'].items():
                out_file.write(f"  vs {opponent}, Wins: {pairwise_stats['wins_against']}, Losses: {pairwise_stats['losses_to']}, "
                               f"Avg Points Scored: {pairwise_stats['avg_points_scored']}, Avg Points Against: {pairwise_stats['avg_points_against']}\n")

def print_all_stats(output_file):
    try:
        with open(output_file, 'r') as file:
            print("Tournament Stats:")
            player_stats = {}
            current_player = None

            for line in file:
                if line.startswith("  vs "):  # Pairwise stats
                    if current_player:
                        parts = line.strip().split(',')
                        opponent = parts[0].split('vs ')[1].strip()
                        wins = parts[1].split(': ')[1]
                        losses = parts[2].split(': ')[1]
                        avg_scored = parts[3].split(': ')[1]
                        avg_against = parts[4].split(': ')[1]
                        player_stats[current_player]["opponents"].append(
                            (opponent, wins, losses, avg_scored, avg_against)
                        )
                else:  # Player stats
                    parts = line.strip().split(',')
                    if len(parts) == 5:
                        player = parts[0]
                        wins = parts[1]
                        losses = parts[2]
                        wl_ratio = parts[3]
                        avg_points = parts[4]
                        player_stats[player] = {
                            "wins": wins,
                            "losses": losses,
                            "wl_ratio": wl_ratio,
                            "avg_points": avg_points,
                            "opponents": [],
                        }
                        current_player = player

            # Print the stats
            for player, stats in player_stats.items():
                print(f"\nPlayer: {player}")
                print(f"  Wins: {stats['wins']}, Losses: {stats['losses']}")
                print(f"  W/L Ratio: {float(stats['wl_ratio']):.2f}")
                print(f"  Avg Points: {float(stats['avg_points']):.2f}")
                if stats["opponents"]:
                    print("  Matches:")
                    for opponent, wins, losses, avg_scored, avg_against in stats["opponents"]:
                        print(f"    vs {opponent}:")
                        print(f"      Wins: {wins}, Losses: {losses}")
                        print(f"      Avg Points Scored: {float(avg_scored):.2f}")
                        print(f"      Avg Points Against: {float(avg_against):.2f}")

    except FileNotFoundError:
        print(f"Error: File '{output_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_player_stats(output_file, player_name):
    try:
        with open(output_file, 'r') as file:
            player_stats = None
            pairwise_stats = {}

            for line in file:
                if line.startswith("  vs "):  # Pairwise stats
                    if player_stats:
                        parts = line.strip().split(',')
                        opponent = parts[0].split('vs ')[1].strip()
                        if opponent == player_name:
                            continue  # Skip self-references
                        wins = int(parts[1].split(': ')[1])
                        losses = int(parts[2].split(': ')[1])
                        avg_scored = float(parts[3].split(': ')[1])
                        avg_against = float(parts[4].split(': ')[1])

                        # Aggregate stats for the same opponent
                        if opponent in pairwise_stats:
                            pairwise_stats[opponent]['wins'] += wins
                            pairwise_stats[opponent]['losses'] += losses
                            pairwise_stats[opponent]['avg_scored'] += avg_scored
                            pairwise_stats[opponent]['avg_against'] += avg_against
                            pairwise_stats[opponent]['matches'] += 1
                        else:
                            pairwise_stats[opponent] = {
                                'wins': wins,
                                'losses': losses,
                                'avg_scored': avg_scored,
                                'avg_against': avg_against,
                                'matches': 1,
                            }
                else:  # Player stats
                    parts = line.strip().split(',')
                    if len(parts) == 5 and parts[0] == player_name:
                        wins = parts[1]
                        losses = parts[2]
                        wl_ratio = parts[3]
                        avg_points = parts[4]
                        player_stats = {
                            "wins": wins,
                            "losses": losses,
                            "wl_ratio": wl_ratio,
                            "avg_points": avg_points,
                        }

            if not player_stats:
                print(f"No stats found for player '{player_name}'.")
                return

            # Print the stats
            print(f"Player: {player_name}")
            print(f"  Wins: {player_stats['wins']}, Losses: {player_stats['losses']}")
            print(f"  W/L Ratio: {float(player_stats['wl_ratio']):.2f}")
            print(f"  Avg Points: {float(player_stats['avg_points']):.2f}")
            if pairwise_stats:
                print("  Matches:")
                for opponent, stats in pairwise_stats.items():
                    avg_points_scored = stats['avg_scored'] / stats['matches']
                    avg_points_against = stats['avg_against'] / stats['matches']
                    print(f"    vs {opponent}:")
                    print(f"      Wins: {stats['wins']}, Losses: {stats['losses']}")
                    print(f"      Avg Points Scored: {avg_points_scored:.2f}")
                    print(f"      Avg Points Against: {avg_points_against:.2f}")

    except FileNotFoundError:
        print(f"Error: File '{output_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

pf = "player_stats.txt"


#Code already ran:
while False:
    process_tournament("P11.txt", tf)
    process_tournament("P12.txt", tf)
    process_tournament("P13.txt", tf)
    process_tournament("P14.txt", tf)
    process_tournament("P15.txt", tf)
    process_tournament("P16.txt", tf)

    process_tournament("P21.txt", tf)
    process_tournament("P22.txt", tf)
    process_tournament("P23.txt", tf)
    process_tournament("P24.txt", tf)

    process_tournament("P31.txt", tf)
    process_tournament("P32.txt", tf)
    process_tournament("P33.txt", tf)
    process_tournament("P34.txt", tf)
    process_tournament("P35.txt", tf)
    process_tournament("P36.txt", tf)

    process_tournament("P41.txt", pf)
    process_tournament("P42.txt", pf)
    process_tournament("P43.txt", pf)
    process_tournament("P44.txt", pf)
    process_tournament("P45.txt", pf)
    process_tournament("P46.txt", pf)
    process_tournament("P47.txt", pf)
    process_tournament("P48.txt", pf)
    process_tournament("P49.txt", pf)
    process_tournament("P410.txt", pf)
    process_tournament("P411.txt", pf)
    break

print_all_stats(pf)
