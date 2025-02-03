import math

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

def load_players(filename):
    players = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            name = parts[0]
            rating = float(parts[1])
            rd = float(parts[2])
            players[name] = {
                "rating": rating,
                "rd": rd
            }
    return players

def update_ratings(player1, player2, score1, score2):
    global players
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

def add_player(file_name, player_name):
    try:
        default_rating = 1500
        default_rd = 350

        with open(file_name, "a") as file:
            file.write(f"{player_name} {default_rating} {default_rd}\n")
        print(f"Player '{player_name}' has been added to the file with rating {default_rating} and RD {default_rd}.")
        print("")

    except Exception as e:
        print(f"An error occurred: {e}")

def save_players_to_file(filename):
    try:
        sorted_players = sorted(players.items(), key=lambda x: x[1]['rating'], reverse=True)

        with open(filename, "w") as file:
            for player, stats in sorted_players:
                file.write(f"{player} {stats['rating']} {stats['rd']:.2f}\n")
    except Exception as e:
        print(f"An error occurred while saving players to file: {e}")

def run_tournament(tournament_file, player_file):
    global players
    players = load_players(player_file)
    print(f"Running tournament with filename {tournament_file}.")
    print("")
    print("-" * 50)
    print("")
    with open(tournament_file, "r") as file:
        for line in file:
            player1, player2, score1, score2 = line.strip().split()

            r1, rd1 = players[player1]["rating"], players[player1]["rd"]
            r2, rd2 = players[player2]["rating"], players[player2]["rd"]
            expected1 = expected_score(r1, r2, rd2)
            expected2 = expected_score(r2, r1, rd1)
            update_ratings(player1, player2, int(score1), int(score2))
    save_players_to_file(player_file)
    print("Updated Player Ratings and RDs:")
    for player, stats in players.items():
        print(f"{player}: Rating = {stats['rating']}, RD = {stats['rd']}")

def print_players_by_elo(file_path):
    try:
        players = []
        with open(file_path, "r") as file:
            for line in file:
                name, rating, rd = line.strip().split()
                players.append({"name": name, "rating": float(rating), "rd": float(rd)})

        players.sort(key=lambda x: x["rating"], reverse=True)

        print("")
        print("*" * 45)
        print("Players sorted by elo rating:")
        print(f"{'Rank':<5} {'Name':<20} {'Rating':<10} {'RD':<10}")
        print("-" * 45)
        for rank, player in enumerate(players, start=1):
            print(f"{rank:<5} {player['name']:<20} {player['rating']:<10.1f} {player['rd']:<10.1f}")
        print("")
        print("*" * 45)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def adjust_rd(filename, days):
    try:
        with open(filename, "r") as file:
            players = []
            for line in file:
                name, rating, rd = line.strip().split()
                players.append({
                    "name": name,
                    "rating": float(rating),
                    "rd": float(rd)
                })

        rds = sorted(player["rd"] for player in players)
        rds2 = [value for value in rds if value < 175]
        print(rds2)
        n = len(rds2)
        if n % 2 == 1:
            median_rd = rds2[n // 2]
        else:
            median_rd = (rds2[n // 2 - 1] + rds2[n // 2]) / 2
        print("")
        print("*" *50)
        print("Updating player RD:s")
        print(f"Median RD: {median_rd}")

        c = math.sqrt((350**2 - median_rd**2) / 365)
        print(f"Decay factor (c): {c}")
        print("")

        for player in players:
            old_rd = player["rd"]
            new_rd = math.sqrt(old_rd**2 + c**2 * days)
            player["rd"] = min(new_rd, 350)
            print(f"Updated {player['name']}s RD from {old_rd} to {new_rd}!")

        with open(filename, "w") as file:
            for player in players:
                file.write(f"{player['name']} {player['rating']} {player['rd']:.2f}\n")
        print("")
        print("Player RDs have been updated based on days since last match.")
        print("")
        print("*" *50)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

pf = "ratingsWL.txt"

#Code already ran:

while True:
    add_player(pf, "Aaro")
    add_player(pf, "Juho")
    add_player(pf, "Riku")
    add_player(pf, "Matias")
    add_player(pf, "Tuomas")

    run_tournament("P11.txt", pf)
    run_tournament("P12.txt", pf)
    run_tournament("P13.txt", pf)
    run_tournament("P14.txt", pf)
    run_tournament("P15.txt", pf)
    run_tournament("P16.txt", pf)

    adjust_rd(pf, 5)
    add_player(pf, "Jesper")

    run_tournament("P21.txt", pf)
    run_tournament("P22.txt", pf)
    run_tournament("P23.txt", pf)
    run_tournament("P24.txt", pf)

    adjust_rd(pf, 4)
    add_player(pf, "Jussi")

    run_tournament("P31.txt", pf)
    run_tournament("P32.txt", pf)
    run_tournament("P33.txt", pf)
    run_tournament("P34.txt", pf)
    run_tournament("P35.txt", pf)
    run_tournament("P36.txt", pf)

    adjust_rd(pf, 7)

    run_tournament("P41.txt", pf)
    run_tournament("P42.txt", pf)
    run_tournament("P43.txt", pf)
    run_tournament("P44.txt", pf)
    run_tournament("P45.txt", pf)
    run_tournament("P46.txt", pf)
    run_tournament("P47.txt", pf)
    run_tournament("P48.txt", pf)
    run_tournament("P49.txt", pf)
    run_tournament("P410.txt", pf)
    run_tournament("P411.txt", pf)

    adjust_rd(pf, 3)

    run_tournament("P51.txt", pf)
    run_tournament("P52.txt", pf)
    run_tournament("P53.txt", pf)
    run_tournament("P54.txt", pf)
    run_tournament("P55.txt", pf)
    run_tournament("P56.txt", pf)
    run_tournament("P57.txt", pf)
    run_tournament("P58.txt", pf)


    adjust_rd(pf, 2)

    add_player(pf, "Samuel")
    add_player(pf, "Elias")

    run_tournament("R11.txt", pf)
    run_tournament("R12.txt", pf)
    run_tournament("R13.txt", pf)
    run_tournament("R14.txt", pf)
    run_tournament("R15.txt", pf)
    run_tournament("R16.txt", pf)
    run_tournament("R17.txt", pf)
    break